import os
import json
from datetime import datetime

GENERATED_DIR = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "generated"
)
HISTORY_FILE = os.path.join(GENERATED_DIR, "creation_history.json")


def load_creation_history():
    if not os.path.exists(HISTORY_FILE):
        return []

    try:
        with open(HISTORY_FILE, "r") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError):
        return []


def save_creation(prompt, tempo, result):
    os.makedirs(GENERATED_DIR, exist_ok=True)
    history = load_creation_history()

    creation = {
        "id": result["id"],
        "title": f"Musegen Composition {len(history) + 1}",
        "prompt": prompt,
        "tempo": int(tempo),
        "genre": result.get("genre", "Classical"),
        "mood": result.get("mood", "Happy"),
        "instruments": result.get("instruments", ["Piano"]),
        "midi_filename": result["midi_filename"],
        "wav_filename": result["wav_filename"],
        "duration": result["duration"],
        "active_cells": result["active_cells"],
        "track_notes": result["track_notes"],
        "created_at": datetime.now().isoformat(timespec="seconds")
    }

    history.insert(0, creation)

    with open(HISTORY_FILE, "w") as file:
        json.dump(history, file, indent=4)

    return creation
