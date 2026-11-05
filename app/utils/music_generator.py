
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

SOUNDFONT_PATH = "/usr/share/sounds/sf2/FluidR3_GM.sf2"

DEVICE = torch.device(
    "cuda" if torch.cuda.is_available() else "cpu"
)

_generator = None

# General MIDI instrument programs (0-127)
INSTRUMENTS = {
    "Piano": 0,
    "Bright Piano": 1,
    "Music Box": 10,
    "Guitar": 24,
    "Acoustic Guitar": 25,
    "Bass": 32,
    "Violin": 40,
    "Viola": 41,
    "Cello": 42,
    "Strings": 48,
    "Choir": 52,
    "Trumpet": 56,
    "Flute": 73,
    "Synth Lead": 80,
    "Synth Pad": 89
}

GENRES = ["Classical", "Pop", "Jazz", "EDM", "Lo-fi"]
MOODS = ["Happy", "Sad", "Romantic", "Energetic"]


def load_generator():
    global _generator

    if _generator is None:
        if not os.path.exists(CHECKPOINT_PATH):
            raise FileNotFoundError(
                f"Model checkpoint not found: {CHECKPOINT_PATH}"
            )

        _generator = MusicForgeGenerator(
            latent_dim=128
        ).to(DEVICE)

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


def generate_music(
    tempo=120,
    threshold=0.5,
    duration=30,
    instruments=None,
    genre="Classical",
    mood="Happy"
):
    tempo = int(tempo)
    duration = float(duration)

    if not 60 <= tempo <= 180:
        raise ValueError("Tempo must be between 60 and 180 BPM.")

    if not 10 <= duration <= 180:
        raise ValueError("Duration must be between 10 and 180 seconds.")

    if genre not in GENRES:
        raise ValueError("Invalid genre.")

    if mood not in MOODS:
        raise ValueError("Invalid mood.")

    if instruments is None:
        instruments = ["Piano", "Violin", "Strings"]

    if isinstance(instruments, str):
        instruments = [instruments]

    if len(instruments) < 1:
        raise ValueError("Select at least one instrument.")

    if len(set(instruments)) != len(instruments):
        raise ValueError("Duplicate instruments are not allowed.")

    for name in instruments:
        if name not in INSTRUMENTS:
            raise ValueError(f"Unsupported instrument: {name}")

    if not os.path.exists(SOUNDFONT_PATH):
        raise FileNotFoundError(
            f"SoundFont not found: {SOUNDFONT_PATH}"
        )

    os.makedirs(GENERATED_DIR, exist_ok=True)

    model = load_generator()

    noise = torch.randn(1, 128, device=DEVICE)

    with torch.no_grad():
        logits = model(noise)
        probabilities = torch.sigmoid(logits)
        piano_roll = (
            probabilities >= threshold
        ).cpu().numpy()[0]

    if piano_roll.shape != (3, 88, 32):
        raise RuntimeError(
            f"Unexpected model output shape: {piano_roll.shape}"
        )

    composition_id = uuid.uuid4().hex[:12]

    midi_filename = f"musegen_{composition_id}.mid"
    wav_filename = f"musegen_{composition_id}.wav"

    midi_path = os.path.join(GENERATED_DIR, midi_filename)
    wav_path = os.path.join(GENERATED_DIR, wav_filename)

    midi = pretty_midi.PrettyMIDI(
        initial_tempo=tempo
    )

    # Scale the original 16-second pattern according to tempo.
    seconds_per_step = 0.5 * (120.0 / tempo)
    pattern_duration = 32 * seconds_per_step

    # Mood affects note velocity as a lightweight arrangement setting.
    mood_velocity = {
        "Happy": 100,
        "Sad": 65,
        "Romantic": 78,
        "Energetic": 115
    }

    base_velocity = mood_velocity[mood]

    for track_index, instrument_name in enumerate(instruments):
        instrument = pretty_midi.Instrument(
            program=INSTRUMENTS[instrument_name],
            name=instrument_name
        )

        roll = piano_roll[track_index % 3]

        for pitch_index in range(88):
            active = np.where(roll[pitch_index] > 0)[0]

            if len(active) == 0:
                continue

            groups = np.split(
                active,
                np.where(np.diff(active) > 1)[0] + 1
            )

            for group in groups:
                start_step = int(group[0])
                end_step = int(group[-1]) + 1

                original_start = start_step * seconds_per_step
                original_end = end_step * seconds_per_step

                repetition = 0

                while True:
                    start = original_start + repetition * pattern_duration

                    if start >= duration:
                        break

                    end = min(
                        original_end + repetition * pattern_duration,
                        duration
                    )

                    if end > start:
                        velocity = min(
                            127,
                            max(1, base_velocity)
                        )

                        instrument.notes.append(
                            pretty_midi.Note(
                                velocity=velocity,
                                pitch=pitch_index + 21,
                                start=start,
                                end=end
                            )
                        )

                    repetition += 1

        midi.instruments.append(instrument)

    midi.write(midi_path)

    # Render audio using the installed General MIDI SoundFont.
    audio = midi.fluidsynth(
        fs=22050,
        sf2_path=SOUNDFONT_PATH
    )

    if len(audio) == 0:
        raise RuntimeError("Audio rendering failed.")

    # Trim or pad audio to the exact requested duration.
    target_samples = int(duration * 22050)

    if len(audio) > target_samples:
        audio = audio[:target_samples]
    elif len(audio) < target_samples:
        audio = np.pad(
            audio,
            (0, target_samples - len(audio))
        )

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
            int(piano_roll[i % 3].sum())
            for i in range(len(instruments))
        ],
        "genre": genre,
        "mood": mood,
        "instruments": instruments,
        "tempo": tempo
    }
