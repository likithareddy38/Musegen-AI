
import os
from flask import Flask, render_template, jsonify, request, send_from_directory

from app.utils.music_generator import generate_music
from app.utils.midi_editor import midi_to_piano_roll
from app.utils.creation_history import load_creation_history, save_creation
from app.utils.creation_history import save_creation

app = Flask(__name__)

GENERATED_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "generated"
)


@app.route("/")
def home():
    return render_template("index.html", page="home")


@app.route("/studio")
def studio():
    return render_template("studio.html", page="studio")


@app.route("/creations")
def creations():
    history = load_creation_history()

    total = len(history)
    total_duration = sum(float(item.get("duration", 0)) for item in history)
    average_tempo = (
        round(sum(int(item.get("tempo", 120)) for item in history) / total)
        if total else 0
    )
    total_active_cells = sum(
        int(item.get("active_cells", 0)) for item in history
    )

    return render_template(
        "creations.html",
        page="creations",
        total_compositions=total,
        total_duration=total_duration,
        average_tempo=average_tempo,
        total_active_cells=total_active_cells
    )


@app.route("/player")
def player():
    return render_template("player.html", page="player")


@app.route("/exports")
def exports():
    return render_template("exports.html", page="exports")


@app.route("/about")
def about():
    return render_template("about.html", page="about")


@app.route("/api/generate", methods=["POST"])
def api_generate():
    try:
        data = request.get_json(silent=True) or {}

        tempo = int(data.get("tempo", 120))

        if not 60 <= tempo <= 180:
            return jsonify({
                "success": False,
                "error": "Tempo must be between 60 and 180 BPM."
            }), 400

        result = generate_music(tempo=tempo)
        creation = save_creation(
            prompt=data.get("prompt", ""),
            tempo=tempo,
            result=result
        )

        return jsonify({
            "success": True,
            "message": "Your composition was generated successfully!",
            "id": result["id"],
            "title": creation["title"],
            "prompt": creation["prompt"],
            "tempo": creation["tempo"],
            "created_at": creation["created_at"],
            "midi_url": f"/generated/{result['midi_filename']}",
            "audio_url": f"/generated/{result['wav_filename']}",
            "duration": result["duration"],
            "active_cells": result["active_cells"],
            "track_notes": result["track_notes"]
        })

    except Exception as error:
        app.logger.exception("Music generation failed")

        return jsonify({
            "success": False,
            "error": str(error)
        }), 500



@app.route("/api/creations", methods=["GET"])
def api_creations():
    try:
        history = load_creation_history()

        creations = []
        for item in history:
            creation = dict(item)
            creation["audio_url"] = (
                f"/generated/{creation['wav_filename']}"
            )
            creation["midi_url"] = (
                f"/generated/{creation['midi_filename']}"
            )
            creations.append(creation)

        return jsonify({
            "success": True,
            "count": len(creations),
            "creations": creations
        })

    except Exception as error:
        app.logger.exception("Could not load creation history")
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.route("/api/creations/<creation_id>", methods=["DELETE"])
def api_delete_creation(creation_id):
    try:
        history = load_creation_history()

        creation = next(
            (item for item in history if item["id"] == creation_id),
            None
        )

        if creation is None:
            return jsonify({
                "success": False,
                "error": "Creation not found."
            }), 404

        generated_dir = GENERATED_DIR

        for key in ["midi_filename", "wav_filename"]:
            filename = os.path.basename(creation[key])
            path = os.path.join(generated_dir, filename)

            if os.path.isfile(path):
                os.remove(path)

        history = [
            item for item in history
            if item["id"] != creation_id
        ]

        history_path = os.path.join(
            generated_dir, "creation_history.json"
        )

        with open(history_path, "w") as file:
            import json
            json.dump(history, file, indent=4)

        return jsonify({
            "success": True,
            "message": "Composition deleted successfully."
        })

    except Exception as error:
        app.logger.exception("Could not delete composition")
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500


@app.route("/api/statistics", methods=["GET"])
def api_statistics():
    try:
        history = load_creation_history()

        total = len(history)
        total_duration = sum(
            float(item.get("duration", 0)) for item in history
        )
        average_tempo = (
            round(sum(int(item.get("tempo", 120)) for item in history) / total)
            if total else 0
        )
        total_active_cells = sum(
            int(item.get("active_cells", 0)) for item in history
        )

        return jsonify({
            "success": True,
            "total_compositions": total,
            "total_duration": round(total_duration, 2),
            "average_tempo": average_tempo,
            "total_active_cells": total_active_cells
        })

    except Exception as error:
        app.logger.exception("Statistics calculation failed")
        return jsonify({
            "success": False,
            "error": str(error)
        }), 500

@app.route("/generated/<path:filename>")
def generated_file(filename):
    return send_from_directory(
        GENERATED_DIR,
        filename,
        as_attachment=False
    )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)


@app.route("/editor")
def editor():
    return render_template("editor.html", page="editor")



@app.route("/api/editor/compositions", methods=["GET"])
def editor_compositions():
    history = load_creation_history()

    compositions = []

    for item in history:
        compositions.append({
            "id": item.get("id"),
            "title": item.get("title", "Untitled Composition"),
            "tempo": item.get("tempo", 120),
            "midi_filename": item.get("midi_filename"),
            "track_notes": item.get("track_notes", []),
            "created_at": item.get("created_at")
        })

    return jsonify({"compositions": compositions})



@app.route("/api/editor/load/<creation_id>", methods=["GET"])
def load_editor_composition(creation_id):
    history = load_creation_history()

    composition = next(
        (item for item in history if item.get("id") == creation_id),
        None
    )

    if composition is None:
        return jsonify({"error": "Composition not found."}), 404

    midi_filename = composition.get("midi_filename")

    if not midi_filename or os.path.basename(midi_filename) != midi_filename:
        return jsonify({"error": "Invalid MIDI filename."}), 400

    midi_path = os.path.join(GENERATED_DIR, midi_filename)

    if not os.path.isfile(midi_path):
        return jsonify({"error": "MIDI file not found."}), 404

    try:
        piano_roll = midi_to_piano_roll(midi_path)

        return jsonify({
            "id": creation_id,
            "title": composition.get("title"),
            "tempo": composition.get("tempo", 120),
            "piano_roll": piano_roll.tolist()
        })

    except Exception as error:
        app.logger.exception("Could not load composition")
        return jsonify({"error": "Could not read MIDI composition."}), 500



@app.route("/api/editor/export", methods=["POST"])
def export_editor_midi():
    import numpy as np
    from app.utils.midi_editor import piano_roll_to_midi

    try:
        data = request.get_json(silent=True) or {}

        piano_roll = np.asarray(
            data.get("piano_roll"),
            dtype=np.float32
        )

        if piano_roll.shape != (3, 88, 32):
            return jsonify({
                "error": "Expected piano roll dimensions (3, 88, 32)."
            }), 400

        if not np.isfinite(piano_roll).all():
            return jsonify({
                "error": "Piano roll contains invalid values."
            }), 400

        if not np.isin(piano_roll, [0, 1]).all():
            return jsonify({
                "error": "Piano roll must contain only 0 and 1."
            }), 400

        tempo = float(data.get("tempo", 120))

        if not 30 <= tempo <= 300:
            return jsonify({
                "error": "Tempo must be between 30 and 300 BPM."
            }), 400

        result = piano_roll_to_midi(
            piano_roll,
            tempo=tempo
        )

        return jsonify({
            "success": True,
            "filename": result["filename"],
            "download_url": f"/generated/{result['filename']}",
            "tracks": result["tracks"],
            "notes": result["notes"]
        })

    except (ValueError, TypeError):
        return jsonify({
            "error": "Invalid piano-roll data or tempo."
        }), 400

    except Exception:
        app.logger.exception("MIDI export failed")
        return jsonify({
            "error": "Could not export MIDI file."
        }), 500

