document.addEventListener("DOMContentLoaded", () => {
    const $ = id => document.getElementById(id);
    const grid = $("piano-grid");
    const labels = $("piano-labels");
    const steps = $("step-labels");
    if (!grid || !labels || !steps) return;

    const MAX_TRACKS = 15;
    const noteNames = ["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"];

    const instruments = [
        ["Piano",0],["Bright Piano",1],["Music Box",10],
        ["Guitar",24],["Acoustic Guitar",25],["Bass",32],
        ["Violin",40],["Viola",41],["Cello",42],["Strings",48],
        ["Choir",52],["Trumpet",56],["Flute",73],
        ["Synth Lead",80],["Synth Pad",89]
    ];

    let tracks = [];
    let activeTrack = 0;
    let tempo = 120;
    let audioContext = null;
    let activeNodes = [];
    let playbackTimers = [];

    const blankRoll = () =>
        Array.from({length:88}, () => Array(32).fill(0));

    const status = message => {
        $("editor-status").textContent = message;
    };

    function populateInstruments() {
        $("instrument-select").innerHTML = instruments.map(
            ([name, program]) =>
                `<option value="${program}">${name}</option>`
        ).join("");
    }

    function addTrack(name, program) {
        if (tracks.length >= MAX_TRACKS) {
            status("Maximum of 15 instrument tracks reached.");
            return false;
        }
        tracks.push({
            name: String(name || `Track ${tracks.length + 1}`).slice(0,80),
            program: Number(program) || 0,
            roll: blankRoll()
        });
        activeTrack = tracks.length - 1;
        renderAll();
        return true;
    }

    function renderLabels() {
        labels.innerHTML = "";
        for (let row = 87; row >= 0; row--) {
            const pitch = row + 21;
            const name = noteNames[pitch % 12];
            const label = document.createElement("div");
            label.className = "piano-key-label";
            label.textContent = name === "C"
                ? name + (Math.floor(pitch / 12) - 1) : "";
            labels.appendChild(label);
        }
        steps.innerHTML = "";
        for (let i = 0; i < 32; i++) {
            const label = document.createElement("div");
            label.className = "step-label";
            label.textContent = i + 1;
            steps.appendChild(label);
        }
    }

    function renderTracks() {
        const selector = $("track-selector");
        selector.innerHTML = "";
        tracks.forEach((track, index) => {
            const button = document.createElement("button");
            button.className = "track-btn" + (index === activeTrack ? " active" : "");
            button.textContent = `${track.name} · ${index + 1}`;
            button.title = `MIDI program ${track.program}`;
            button.addEventListener("click", () => {
                activeTrack = index;
                renderAll();
            });
            selector.appendChild(button);
        });
        $("track-count").textContent = `Tracks: ${tracks.length} / ${MAX_TRACKS}`;
    }

    function updateNoteCount() {
        if (!tracks.length) {
            $("note-count").textContent = "Notes: 0";
            return;
        }
        const count = tracks[activeTrack].roll.flat()
            .reduce((sum, value) => sum + Number(value), 0);
        $("note-count").textContent =
            `${tracks[activeTrack].name} · ${count} notes`;
    }

    function renderGrid() {
        grid.innerHTML = "";
        if (!tracks.length) {
            updateNoteCount();
            return;
        }

        const roll = tracks[activeTrack].roll;
        for (let row = 87; row >= 0; row--) {
            const pitch = row + 21;
            for (let step = 0; step < 32; step++) {
                const cell = document.createElement("div");
                const pitchClass = pitch % 12;
                cell.className = "piano-cell";
                if ([1,3,6,8,10].includes(pitchClass))
                    cell.classList.add("black-key-row");
                if (pitchClass === 0) cell.classList.add("octave-start");
                if (roll[row][step]) cell.classList.add("active-note");

                cell.dataset.pitch = row;
                cell.dataset.step = step;
                cell.addEventListener("click", () => {
                    roll[row][step] = roll[row][step] ? 0 : 1;
                    cell.classList.toggle("active-note", !!roll[row][step]);
                    updateNoteCount();
                });
                grid.appendChild(cell);
            }
        }
        updateNoteCount();
    }

    function renderAll() {
        renderTracks();
        renderGrid();
    }

    $("add-track").addEventListener("click", () => {
        const option = $("instrument-select").selectedOptions[0];
        if (addTrack(option.textContent, Number(option.value)))
            status(`${option.textContent} track added.`);
    });

    $("remove-track").addEventListener("click", () => {
        if (!tracks.length) return;
        const removed = tracks.splice(activeTrack, 1)[0];
        activeTrack = Math.max(0, Math.min(activeTrack, tracks.length - 1));
        renderAll();
        status(`${removed.name} track removed.`);
    });

    $("clear-track").addEventListener("click", () => {
        if (!tracks.length) return;
        tracks[activeTrack].roll = blankRoll();
        renderGrid();
        status("Current track cleared.");
    });

    $("tempo-control").addEventListener("input", event => {
        tempo = Number(event.target.value);
        $("tempo-value").textContent = `${tempo} BPM`;
    });

    $("zoom-control").addEventListener("input", event => {
        const width = Number(event.target.value);
        document.querySelectorAll(".piano-grid,.step-labels").forEach(el => {
            el.style.gridTemplateColumns = `repeat(32, ${width}px)`;
        });
    });

    async function loadCompositionList() {
        try {
            const response = await fetch("/api/editor/compositions");
            if (!response.ok) throw new Error("Could not load compositions.");
            const data = await response.json();
            $("composition-select").innerHTML =
                '<option value="">Select a composition...</option>';
            (data.compositions || []).forEach(item => {
                const option = document.createElement("option");
                option.value = item.id;
                option.textContent = `${item.title} (${item.tempo} BPM)`;
                $("composition-select").appendChild(option);
            });
        } catch (error) {
            status(error.message);
        }
    }

    $("load-composition").addEventListener("click", async () => {
        const id = $("composition-select").value;
        if (!id) return status("Please select a composition first.");
        try {
            status("Loading composition...");
            const response = await fetch(
                `/api/editor/load/${encodeURIComponent(id)}`
            );
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || "Load failed.");

            tracks = data.piano_roll.map((roll, index) => ({
                name: data.track_names?.[index] || `Track ${index + 1}`,
                program: data.programs?.[index] ?? 0,
                roll
            }));
            activeTrack = 0;
            tempo = Number(data.tempo || 120);
            $("tempo-control").value = tempo;
            $("tempo-value").textContent = `${tempo} BPM`;
            renderAll();
            status(`Loaded ${tracks.length} instrument track(s).`);
        } catch (error) {
            status(error.message);
        }
    });

    function stopComposition() {
        playbackTimers.forEach(clearTimeout);
        playbackTimers = [];
        activeNodes.forEach(node => {
            try { node.stop(); } catch (_) {}
        });
        activeNodes = [];
        $("play-composition").textContent = "▶ Play";
    }

    async function playComposition() {
        stopComposition();
        if (!tracks.length) return status("Add or load a track first.");
        try {
            const AudioClass = window.AudioContext || window.webkitAudioContext;
            if (!AudioClass) throw new Error("Web Audio is unavailable.");
            if (!audioContext || audioContext.state === "closed")
                audioContext = new AudioClass();
            await audioContext.resume();

            const secondsPerStep = 30 / tempo;
            const startTime = audioContext.currentTime + 0.1;

            tracks.forEach((track, trackIndex) => {
                track.roll.forEach((row, pitchIndex) => {
                    let step = 0;
                    while (step < 32) {
                        if (!row[step]) { step++; continue; }
                        const start = step;
                        while (step < 32 && row[step]) step++;
                        const onset = startTime + start * secondsPerStep;
                        const ending = startTime + step * secondsPerStep;
                        const oscillator = audioContext.createOscillator();
                        const gain = audioContext.createGain();
                        oscillator.type = ["triangle","sine","sawtooth","square"][trackIndex % 4];
                        oscillator.frequency.value =
                            440 * Math.pow(2, (pitchIndex + 21 - 69) / 12);
                        gain.gain.setValueAtTime(0.0001, onset);
                        gain.gain.linearRampToValueAtTime(0.10, onset + 0.02);
                        gain.gain.setValueAtTime(0.10, Math.max(onset + 0.03, ending - 0.04));
                        gain.gain.linearRampToValueAtTime(0.0001, ending);
                        oscillator.connect(gain);
                        gain.connect(audioContext.destination);
                        oscillator.start(onset);
                        oscillator.stop(ending);
                        activeNodes.push(oscillator);
                    }
                });
            });

            $("play-composition").textContent = "▶ Playing...";
            playbackTimers.push(setTimeout(() => {
                activeNodes = [];
                playbackTimers = [];
                $("play-composition").textContent = "▶ Play";
            }, 32 * secondsPerStep * 1000 + 500));
            status("Playing all instrument tracks.");
        } catch (error) {
            status("Playback error: " + error.message);
        }
    }

    $("play-composition").addEventListener("click", playComposition);
    $("stop-composition").addEventListener("click", stopComposition);

    $("export-midi").addEventListener("click", async () => {
        if (!tracks.length) return status("Add or load a track before exporting.");
        const button = $("export-midi");
        button.disabled = true;
        button.textContent = "Exporting...";
        try {
            const response = await fetch("/api/editor/export", {
                method: "POST",
                headers: {"Content-Type":"application/json"},
                body: JSON.stringify({
                    piano_roll: tracks.map(track => track.roll),
                    track_names: tracks.map(track => track.name),
                    programs: tracks.map(track => track.program),
                    tempo
                })
            });
            const data = await response.json();
            if (!response.ok) throw new Error(data.error || "Export failed.");
            const link = document.createElement("a");
            link.href = data.download_url;
            link.download = data.filename;
            document.body.appendChild(link);
            link.click();
            link.remove();
            status(`Exported ${data.tracks} tracks and ${data.notes} notes.`);
        } catch (error) {
            status(error.message);
        } finally {
            button.disabled = false;
            button.textContent = "⬇ Export MIDI";
        }
    });

    populateInstruments();
    renderLabels();
    renderAll();
    loadCompositionList();

    window.musegenEditor = {
        get tracks() { return tracks; },
        get tempo() { return tempo; }
    };
});
