
document.addEventListener("DOMContentLoaded", function () {

    const grid = document.getElementById("piano-grid");
    const labels = document.getElementById("piano-labels");
    const steps = document.getElementById("step-labels");
    const noteCount = document.getElementById("note-count");

    if (!grid || !labels || !steps) return;

    const TRACKS = ["Melody", "Bridge", "Piano"];

    let activeTrack = 0;

    // Three tracks, 88 pitches, 32 time steps.
    const pianoRoll = Array.from(
        { length: 3 },
        () => Array.from(
            { length: 88 },
            () => Array(32).fill(0)
        )
    );

    const noteNames = [
        "C", "C#", "D", "D#", "E", "F",
        "F#", "G", "G#", "A", "A#", "B"
    ];

    function renderLabels() {
        labels.innerHTML = "";

        for (let row = 87; row >= 0; row--) {
            const pitch = row + 21;
            const octave = Math.floor(pitch / 12) - 1;
            const name = noteNames[pitch % 12];

            const label = document.createElement("div");
            label.className = "piano-key-label";
            label.textContent = name === "C"
                ? name + octave
                : "";

            labels.appendChild(label);
        }

        steps.innerHTML = "";

        for (let step = 0; step < 32; step++) {
            const label = document.createElement("div");
            label.className = "step-label";
            label.textContent = step + 1;
            steps.appendChild(label);
        }
    }

    function renderGrid() {
        grid.innerHTML = "";

        for (let row = 87; row >= 0; row--) {
            const pitch = row + 21;

            for (let step = 0; step < 32; step++) {
                const cell = document.createElement("div");

                cell.className = "piano-cell";

                const pitchClass = pitch % 12;

                if ([1, 3, 6, 8, 10].includes(pitchClass)) {
                    cell.classList.add("black-key-row");
                }

                if (pitchClass === 0) {
                    cell.classList.add("octave-start");
                }

                if (pianoRoll[activeTrack][row][step]) {
                    cell.classList.add("active-note");
                }

                cell.dataset.pitch = row;
                cell.dataset.step = step;

                cell.addEventListener("click", function () {
                    const p = Number(this.dataset.pitch);
                    const s = Number(this.dataset.step);

                    pianoRoll[activeTrack][p][s] =
                        pianoRoll[activeTrack][p][s] ? 0 : 1;

                    this.classList.toggle(
                        "active-note",
                        Boolean(pianoRoll[activeTrack][p][s])
                    );

                    updateNoteCount();
                });

                grid.appendChild(cell);
            }
        }

        updateNoteCount();
    }

    function updateNoteCount() {
        const count = pianoRoll[activeTrack]
            .flat()
            .reduce((total, value) => total + value, 0);

        noteCount.textContent =
            TRACKS[activeTrack] + " Notes: " + count;
    }

    document.querySelectorAll(".track-btn").forEach(button => {
        button.addEventListener("click", function () {
            activeTrack = Number(this.dataset.track);

            document.querySelectorAll(".track-btn")
                .forEach(btn => btn.classList.remove("active"));

            this.classList.add("active");

            renderGrid();
        });
    });

    const clearButton = document.getElementById("clear-track");

    if (clearButton) {
        clearButton.addEventListener("click", function () {
            pianoRoll[activeTrack] =
                Array.from({ length: 88 }, () => Array(32).fill(0));

            renderGrid();
        });
    }

    renderLabels();
    renderGrid();

    // Expose editor state for the upcoming export integration.
    

    // Load saved compositions into the selector.
    const compositionSelect =
        document.getElementById("composition-select");

    const loadCompositionButton =
        document.getElementById("load-composition");

    async function loadCompositionList() {
        if (!compositionSelect) return;

        try {
            const response = await fetch(
                "/api/editor/compositions"
            );

            if (!response.ok) {
                throw new Error("Could not retrieve compositions.");
            }

            const data = await response.json();

            compositionSelect.innerHTML =
                '<option value="">Select a composition...</option>';

            (data.compositions || []).forEach(item => {
                const option = document.createElement("option");

                option.value = item.id;
                option.textContent =
                    `${item.title} (${item.tempo} BPM)`;

                compositionSelect.appendChild(option);
            });

        } catch (error) {
            console.error("Composition list error:", error);
        }
    }

    if (loadCompositionButton) {
        loadCompositionButton.addEventListener("click", async function () {
            const compositionId = compositionSelect.value;

            if (!compositionId) {
                alert("Please select a composition first.");
                return;
            }

            try {
                const response = await fetch(
                    `/api/editor/load/${encodeURIComponent(compositionId)}`
                );

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || "Composition loading failed.");
                }

                for (let track = 0; track < 3; track++) {
                    pianoRoll[track] = data.piano_roll[track];
                }

                renderGrid();

                alert("Composition loaded successfully!");

            } catch (error) {
                console.error(error);
                alert(error.message);
            }
        });
    }

    loadCompositionList();


    

    // MUSEGEN PIANO ROLL PLAYBACK
    let playbackTimers = [];
    let activeAudioNodes = [];
    let audioContext = null;

    function stopComposition() {
        playbackTimers.forEach(timer => clearTimeout(timer));
        playbackTimers = [];

        activeAudioNodes.forEach(node => {
            try {
                node.stop();
            } catch (error) {}
        });

        activeAudioNodes = [];

        const playButton =
            document.getElementById("play-composition");

        if (playButton) playButton.textContent = "▶ Play";
    }

    async function playComposition() {
        stopComposition();

        const playButton =
            document.getElementById("play-composition");

        try {
            const AudioContextClass =
                window.AudioContext || window.webkitAudioContext;

            if (!AudioContextClass) {
                throw new Error("Web Audio is not supported by this browser.");
            }

            if (!audioContext || audioContext.state === "closed") {
                audioContext = new AudioContextClass();
            }

            await audioContext.resume();

            const secondsPerStep = 0.5;
            const startTime = audioContext.currentTime + 0.1;

            for (let track = 0; track < 3; track++) {
                for (let pitch = 0; pitch < 88; pitch++) {
                    let step = 0;

                    while (step < 32) {
                        if (!pianoRoll[track][pitch][step]) {
                            step++;
                            continue;
                        }

                        const noteStart = step;
                        while (
                            step < 32 &&
                            pianoRoll[track][pitch][step]
                        ) {
                            step++;
                        }

                        const noteEnd = step;
                        const frequency =
                            440 * Math.pow(2, (pitch + 21 - 69) / 12);

                        const oscillator =
                            audioContext.createOscillator();

                        const gain = audioContext.createGain();

                        oscillator.type =
                            track === 0 ? "triangle" :
                            track === 1 ? "sine" : "sawtooth";

                        oscillator.frequency.value = frequency;

                        const onset =
                            startTime + noteStart * secondsPerStep;

                        const ending =
                            startTime + noteEnd * secondsPerStep;

                        gain.gain.setValueAtTime(0.0001, onset);
                        gain.gain.linearRampToValueAtTime(0.12, onset + 0.02);
                        gain.gain.setValueAtTime(0.12, Math.max(onset + 0.03, ending - 0.04));
                        gain.gain.linearRampToValueAtTime(0.0001, ending);

                        oscillator.connect(gain);
                        gain.connect(audioContext.destination);

                        oscillator.start(onset);
                        oscillator.stop(ending);

                        activeAudioNodes.push(oscillator);
                    }
                }
            }

            if (playButton) playButton.textContent = "▶ Playing...";

            const finishTimer = setTimeout(() => {
                activeAudioNodes = [];
                playbackTimers = [];

                if (playButton) playButton.textContent = "▶ Play";
            }, 32 * secondsPerStep * 1000 + 500);

            playbackTimers.push(finishTimer);

        } catch (error) {
            console.error("Playback error:", error);
            alert("Playback failed: " + error.message);
        }
    }

    document.getElementById("play-composition")
        ?.addEventListener("click", playComposition);

    document.getElementById("stop-composition")
        ?.addEventListener("click", stopComposition);


    

    // EXPORT EDITED PIANO ROLL AS MIDI
    const exportButton = document.getElementById("export-midi");

    if (exportButton) {
        exportButton.addEventListener("click", async function () {
            try {
                exportButton.disabled = true;
                exportButton.textContent = "Exporting...";

                const response = await fetch("/api/editor/export", {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/json"
                    },
                    body: JSON.stringify({
                        piano_roll: pianoRoll,
                        tempo: 120
                    })
                });

                const data = await response.json();

                if (!response.ok) {
                    throw new Error(data.error || "MIDI export failed.");
                }

                const downloadLink = document.createElement("a");
                downloadLink.href = data.download_url;
                downloadLink.download = data.filename;

                document.body.appendChild(downloadLink);
                downloadLink.click();
                downloadLink.remove();

                alert("Edited MIDI exported successfully!");

            } catch (error) {
                console.error("MIDI export error:", error);
                alert(error.message);
            } finally {
                exportButton.disabled = false;
                exportButton.textContent = "⬇ Export MIDI";
            }
        });
    }


    window.musegenPianoRoll = pianoRoll;

});
