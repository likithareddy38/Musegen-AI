
import os
import uuid
import numpy as np
import pretty_midi

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

GENERATED_DIR = os.path.join(
    PROJECT_DIR, "app", "generated"
)

TRACK_NAMES = ["Melody", "Bridge", "Piano"]
PROGRAMS = [0, 48, 0]

def piano_roll_to_midi(piano_roll, tempo=120):
    piano_roll = np.asarray(piano_roll)

    if piano_roll.shape != (3, 88, 32):
        raise ValueError(
            "Expected piano roll shape (3, 88, 32)."
        )

    if not np.isfinite(piano_roll).all():
        raise ValueError("Piano roll contains invalid values.")

    piano_roll = (piano_roll > 0).astype(np.uint8)

    os.makedirs(GENERATED_DIR, exist_ok=True)

    midi = pretty_midi.PrettyMIDI(
        initial_tempo=float(tempo)
    )

    seconds_per_step = 0.5

    for track_index, track_name in enumerate(TRACK_NAMES):
        instrument = pretty_midi.Instrument(
            program=PROGRAMS[track_index],
            name=track_name
        )

        for pitch_index in range(88):
            active = np.where(
                piano_roll[track_index, pitch_index] > 0
            )[0]

            if len(active) == 0:
                continue

            groups = np.split(
                active,
                np.where(np.diff(active) > 1)[0] + 1
            )

            for group in groups:
                instrument.notes.append(
                    pretty_midi.Note(
                        velocity=90,
                        pitch=pitch_index + 21,
                        start=int(group[0]) * seconds_per_step,
                        end=(int(group[-1]) + 1) * seconds_per_step
                    )
                )

        midi.instruments.append(instrument)

    filename = f"edited_{uuid.uuid4().hex[:12]}.mid"
    filepath = os.path.join(GENERATED_DIR, filename)

    midi.write(filepath)

    return {
        "filename": filename,
        "filepath": filepath,
        "tracks": len(midi.instruments),
        "notes": sum(
            len(track.notes) for track in midi.instruments
        )
    }


def midi_to_piano_roll(midi_path, seconds_per_step=0.5):
    """Convert a three-track MIDI file into a (3, 88, 32) piano roll."""

    if not os.path.exists(midi_path):
        raise FileNotFoundError(midi_path)

    if seconds_per_step <= 0:
        raise ValueError("seconds_per_step must be positive.")

    midi = pretty_midi.PrettyMIDI(midi_path)

    piano_roll = np.zeros((3, 88, 32), dtype=np.uint8)

    track_mapping = {
        "melody": 0,
        "bridge": 1,
        "piano": 2
    }

    for instrument_index, instrument in enumerate(midi.instruments):

        track_name = instrument.name.strip().lower()

        if track_name in track_mapping:
            track_index = track_mapping[track_name]
        elif instrument_index < 3:
            track_index = instrument_index
        else:
            continue

        for note in instrument.notes:

            pitch_index = note.pitch - 21

            if not 0 <= pitch_index < 88:
                continue

            start_step = int(
                round(note.start / seconds_per_step)
            )

            end_step = int(
                round(note.end / seconds_per_step)
            )

            start_step = max(0, min(31, start_step))
            end_step = max(0, min(32, end_step))

            if end_step <= start_step:
                end_step = min(32, start_step + 1)

            piano_roll[
                track_index,
                pitch_index,
                start_step:end_step
            ] = 1

    return piano_roll
