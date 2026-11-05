
import os
import uuid
import numpy as np
import pretty_midi

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "..")
)
GENERATED_DIR = os.path.join(PROJECT_DIR, "generated")
os.makedirs(GENERATED_DIR, exist_ok=True)

# Fallback names/programs for older three-track compositions.
TRACK_NAMES = ["Melody", "Bridge", "Piano"]
PROGRAMS = [0, 48, 0]

def piano_roll_to_midi(
    piano_roll,
    tempo=120,
    track_names=None,
    programs=None
):
    piano_roll = np.asarray(piano_roll)

    if (
        piano_roll.ndim != 3
        or piano_roll.shape[1:] != (88, 32)
        or not 1 <= piano_roll.shape[0] <= 15
    ):
        raise ValueError(
            "Expected piano roll shape (1-15, 88, 32)."
        )

    if not np.isfinite(piano_roll).all():
        raise ValueError("Piano roll contains invalid values.")

    piano_roll = (piano_roll > 0).astype(np.uint8)
    track_count = piano_roll.shape[0]

    track_names = list(track_names or [])
    programs = list(programs or [])

    midi = pretty_midi.PrettyMIDI(
        initial_tempo=float(tempo)
    )

    total_notes = 0
    seconds_per_step = 60.0 / float(tempo) / 2.0

    for track_index in range(track_count):
        name = (
            str(track_names[track_index])[:80]
            if track_index < len(track_names)
            else f"Track {track_index + 1}"
        )

        program = (
            int(programs[track_index])
            if track_index < len(programs)
            else PROGRAMS[track_index]
            if track_index < len(PROGRAMS)
            else 0
        )

        if not 0 <= program <= 127:
            raise ValueError("Invalid MIDI instrument program.")

        instrument = pretty_midi.Instrument(
            program=program,
            name=name
        )

        for pitch_index in range(88):
            row = piano_roll[track_index, pitch_index]
            active_steps = np.flatnonzero(row)

            if len(active_steps) == 0:
                continue

            start_step = previous_step = int(active_steps[0])

            for step in list(active_steps[1:]) + [None]:
                if step is not None and int(step) == previous_step + 1:
                    previous_step = int(step)
                    continue

                start_time = start_step * seconds_per_step
                end_time = (previous_step + 1) * seconds_per_step

                instrument.notes.append(
                    pretty_midi.Note(
                        velocity=90,
                        pitch=pitch_index + 21,
                        start=start_time,
                        end=end_time
                    )
                )
                total_notes += 1

                if step is not None:
                    start_step = previous_step = int(step)

        midi.instruments.append(instrument)

    filename = f"edited_{uuid.uuid4().hex[:12]}.mid"
    filepath = os.path.join(GENERATED_DIR, filename)
    midi.write(filepath)

    return {
        "filename": filename,
        "filepath": filepath,
        "tracks": track_count,
        "notes": total_notes,
        "track_names": [track.name for track in midi.instruments],
        "programs": [track.program for track in midi.instruments]
    }


def midi_to_piano_roll(midi_path, seconds_per_step=0.5):
    """
    Convert every MIDI instrument into a piano roll.
    Returns an array shaped (number_of_tracks, 88, 32).
    """
    midi = pretty_midi.PrettyMIDI(midi_path)

    instruments = midi.instruments[:15]
    if not instruments:
        instruments = [
            pretty_midi.Instrument(program=0, name="Piano")
        ]

    piano_roll = np.zeros(
        (len(instruments), 88, 32),
        dtype=np.uint8
    )

    for track_index, instrument in enumerate(instruments):
        for note in instrument.notes:
            if 21 <= note.pitch <= 108:
                start = max(
                    0,
                    int(note.start / seconds_per_step)
                )
                end = min(
                    32,
                    max(
                        start + 1,
                        int(np.ceil(note.end / seconds_per_step))
                    )
                )

                if start < 32:
                    piano_roll[
                        track_index,
                        note.pitch - 21,
                        start:end
                    ] = 1

    return piano_roll


def midi_track_metadata(midi_path):
    """Return track names and General MIDI program numbers."""
    midi = pretty_midi.PrettyMIDI(midi_path)
    instruments = midi.instruments[:15]

    return {
        "track_names": [
            instrument.name or f"Track {index + 1}"
            for index, instrument in enumerate(instruments)
        ],
        "programs": [
            int(instrument.program)
            for instrument in instruments
        ]
    }
