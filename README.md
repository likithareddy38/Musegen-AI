# 🎵 Musegen AI – AI-Powered Music Generation Studio

**Musegen AI** is an AI-powered music generation web application designed to make music creation easier and more accessible. It provides a creative platform where users can generate music, explore their saved compositions, listen to generated tracks, and work with MIDI-based music editing features.

🌐 **Live Application:** https://musegen-ai.onrender.com

💻 **GitHub Repository:** https://github.com/likithareddy38/Musegen-AI

---

## ✨ Features

- 🎼 **AI Music Generation** – Generate musical compositions using the application's music generation system.
- 🎹 **Music Studio** – Access the music creation interface.
- 🎧 **Music Player** – Listen to generated compositions with playback controls.
- 📚 **Creation History** – Browse saved musical compositions.
- 🎛️ **MIDI Editing** – Work with MIDI-based music editing functionality.
- 📥 **Music Exports** – Access generated music files.
- 📊 **Statistics** – View application statistics.
- 🌐 **Web Interface** – Use the application through a Flask-powered web interface.

## 🛠️ Technologies Used

- Python
- Flask
- PyTorch
- NumPy
- SciPy
- PrettyMIDI
- PyFluidSynth
- SoundFile
- HTML, CSS, JavaScript
- Gunicorn
- Docker
- Render

## 📁 Project Structure

```text
Musegen-AI/
│
├── app/
│   ├── app.py
│   ├── generated/
│   ├── static/
│   │   ├── css/
│   │   └── js/
│   ├── templates/
│   └── utils/
│       ├── music_generator.py
│       ├── creation_history.py
│       └── midi_editor.py
│
├── Dockerfile
├── render.yaml
├── requirements.txt
└── README.md
```

## 🚀 Run Locally

### 1. Clone the repository

```bash
git clone https://github.com/likithareddy38/Musegen-AI.git
cd Musegen-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate it:

**Windows**
```bash
venv\Scripts\activate
```

**Linux / macOS**
```bash
source venv/bin/activate
```

### 3. Install FluidSynth

FluidSynth's native library is required for MIDI audio synthesis.

**Ubuntu / Debian**
```bash
sudo apt-get update
sudo apt-get install -y libfluidsynth3
```

### 4. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 5. Start the application

```bash
python -m flask --app app.app run
```

Open your browser at:

```text
http://127.0.0.1:5000
```

## 🐳 Deployment

Musegen AI is configured for Docker-based deployment on Render.

The repository includes:

- `Dockerfile` – Defines the application environment and system dependencies.
- `render.yaml` – Contains Render service configuration.
- `requirements.txt` – Lists Python dependencies.

Live deployment:

**https://musegen-ai.onrender.com**

## 🎯 Project Objective

The objective of Musegen AI is to explore AI-assisted music creation by combining music generation technologies with an accessible web-based interface.

It aims to provide an interactive environment for creating, listening to, managing, and editing musical compositions.

## 👩‍💻 Author

**Likitha Reddy**

GitHub: https://github.com/likithareddy38

## 📜 License

This project is available for educational and development purposes. Add a license file to the repository if you wish to specify reuse and distribution permissions.

---

⭐ If you find this project interesting, consider starring the repository!

**Experience Musegen AI:** https://musegen-ai.onrender.com
