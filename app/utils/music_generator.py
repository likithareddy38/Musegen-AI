
import os
import uuid
import torch
import numpy as np
import pretty_midi
import soundfile as sf

from app.models.musicforge_model import MusicForgeGenerator

PROJECT_DIR = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

CHECKPOINT_PATH = os.path.join(
    PROJECT_DIR,
    "checkpoints",
    "final",
    "musicforge_preferred_final_55_epochs.pth"
)

GENERATED_DIR = os.path.join(
    PROJECT_DIR, "app", "generated"
)

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

_generator = None


def load_generator():
    global _generator

    if _generator is None:
        _generator = MusicForgeGenerator(latent_dim=128).to(DEVICE)

        checkpoint = torch.load(
            CHECKPOINT_PATH,
            map_location=DEVICE,
            weights_only=False
        )

        _generator.load_state_dict(
            checkpoint["generator_state_dict"]
        )

        _generator.eval()

    return _generator


def generate_music(tempo=120, threshold=0.5):
    os.makedirs(GENERATED_DIR, exist_ok=True)

    model = load_generator()

    noise = torch.randn(1, 128, device=DEVICE)

    with torch.no_grad():
        logits = model(noise)
        probabilities = torch.sigmoid(logits)
        piano_roll = (
            probabilities >= threshold
        ).cpu().numpy()[0]

    composition_id = uuid.uuid4().hex[:12]

    midi_filename = f"musegen_{composition_id}.mid"
    wav_filename = f"musegen_{composition_id}.wav"

    midi_path = os.path.join(
        GENERATED_DIR, midi_filename
    )

    wav_path = os.path.join(
        GENERATED_DIR, wav_filename
    )

    midi = pretty_midi.PrettyMIDI(
        initial_tempo=tempo
    )

    track_names = ["Melody", "Bridge", "Piano"]
    programs = [0, 48, 0]

    seconds_per_step = 0.5

    for track_index, track_name in enumerate(track_names):
        instrument = pretty_midi.Instrument(
            program=programs[track_index],
            name=track_name
        )

        roll = piano_roll[track_index]

        for pitch_index in range(88):
            active = np.where(
                roll[pitch_index] > 0
            )[0]

            if len(active) == 0:
                continue

            groups = np.split(
                active,
                np.where(np.diff(active) > 1)[0] + 1
            )

            for group in groups:
                start = int(group[0]) * seconds_per_step
                end = (int(group[-1]) + 1) * seconds_per_step

                instrument.notes.append(
                    pretty_midi.Note(
                        velocity=90,
                        pitch=pitch_index + 21,
                        start=start,
                        end=end
                    )
                )

        midi.instruments.append(instrument)

    midi.write(midi_path)

    # Render WAV using FluidSynth
    audio = midi.fluidsynth(fs=22050)

    if len(audio) == 0:
        raise RuntimeError("Audio rendering failed.")

    peak = np.max(np.abs(audio))

    if peak > 0:
        audio = audio / peak * 0.9

    sf.write(wav_path, audio, 22050)

    return {
        "id": composition_id,
        "midi_filename": midi_filename,
        "wav_filename": wav_filename,
        "midi_path": midi_path,
        "wav_path": wav_path,
        "duration": round(len(audio) / 22050, 2),
        "active_cells": int(piano_roll.sum()),
        "track_notes": [
            int(track.sum()) for track in piano_roll
        ]
    }
