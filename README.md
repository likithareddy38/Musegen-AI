# 🎵 Musegen AI
### AI-Powered Music Generation and Multi-Track MIDI Editing Platform

![Python](https://img.shields.io/badge/Python-3.11-blue)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-orange)
![Flask](https://img.shields.io/badge/Flask-Backend-black)
![JavaScript](https://img.shields.io/badge/JavaScript-Frontend-yellow)
![Docker](https://img.shields.io/badge/Docker-Containerization-blue)
![Render](https://img.shields.io/badge/Deployment-Render-purple)

**Musegen AI** is a web-based artificial intelligence music generation and editing application that integrates a trained MuseGAN model with a multi-track MIDI editing environment.

The application enables users to generate musical compositions by selecting tempo, duration, instruments, genre, and mood options. It converts generated symbolic music patterns into MIDI files and renders them into playable WAV audio using FluidSynth and a General MIDI SoundFont.

Musegen AI also includes an interactive Piano Roll Editor that allows users to create and remove notes, manage multiple instrument tracks, adjust tempo, and import or export MIDI compositions.

🌐 **Live Application:** https://musegen-ai.onrender.com

📂 **GitHub Repository:** https://github.com/likithareddy38/Musegen-AI

---

## 📌 Table of Contents

1. [Project Overview](#-project-overview)
2. [Problem Statement](#-problem-statement)
3. [Project Objectives](#-project-objectives)
4. [Key Features](#-key-features)
5. [AI Model - MuseGAN](#-ai-model---musegan)
6. [Music Generation Process](#-music-generation-process)
7. [Supported Instruments](#-supported-instruments)
8. [Genre and Mood Options](#-genre-and-mood-options)
9. [MIDI and WAV Audio Processing](#-midi-and-wav-audio-processing)
10. [Piano Roll Editor](#-piano-roll-editor)
11. [System Architecture](#-system-architecture)
12. [Technology Stack](#-technology-stack)
13. [Project Structure](#-project-structure)
14. [Installation and Setup](#-installation-and-setup)
15. [Running the Application](#-running-the-application)
16. [API Overview](#-api-overview)
17. [Docker Configuration](#-docker-configuration)
18. [Deployment on Render](#-deployment-on-render)
19. [Testing and Validation](#-testing-and-validation)
20. [Challenges and Solutions](#-challenges-and-solutions)
21. [Current Implementation Details and Limitations](#-current-implementation-details-and-limitations)
22. [Future Enhancements](#-future-enhancements)
23. [Team Contributions](#-team-contributions)
24. [Acknowledgements](#-acknowledgements)
25. [License](#-license)

---

## 📖 Project Overview

Music creation traditionally requires knowledge of musical instruments, melody, rhythm, harmony, tempo, and digital audio production tools.

Musegen AI aims to simplify this process by combining AI-assisted music generation with an accessible web-based music editing environment.

The application uses an existing trained MuseGAN model to generate symbolic musical patterns. These patterns are processed into MIDI compositions, which can subsequently be converted into WAV audio.

Users can also work with their musical compositions through the built-in Piano Roll Editor.

### Main Components

- **AI Music Generator:** Generates musical patterns using the trained MuseGAN model.
- **Music Studio:** Provides controls for tempo, duration, instruments, genre, and mood.
- **MIDI Processing:** Converts generated musical patterns into MIDI compositions.
- **Audio Synthesis:** Uses FluidSynth and SoundFont samples to render MIDI into WAV audio.
- **Piano Roll Editor:** Provides visual multi-track MIDI editing.
- **Composition History:** Stores generated composition information and selected settings.
- **Web Application:** Connects all components through a Flask backend and browser-based interface.

---

## 🎯 Problem Statement

Traditional music composition can be time-consuming and technically challenging, particularly for beginners.

Some of the major challenges include:

- Requiring musical knowledge to create compositions.
- Spending significant time arranging notes and instruments.
- Difficulty using advanced music production software.
- Needing separate tools for music generation, MIDI editing, and audio rendering.
- Difficulty experimenting with different instrument combinations.

Musegen AI addresses these challenges by providing an integrated environment for AI-assisted music generation and basic MIDI editing.

---

## 🎯 Project Objectives

The primary objectives of Musegen AI are:

1. Integrate a trained MuseGAN model into a web application.
2. Generate symbolic musical compositions using artificial intelligence.
3. Provide configurable tempo and music duration.
4. Support up to 15 selectable instrument tracks.
5. Provide genre and mood selection options.
6. Generate MIDI compositions.
7. Convert MIDI files into playable WAV audio.
8. Develop a multi-track Piano Roll Editor.
9. Support MIDI import and export.
10. Maintain composition history and metadata.
11. Provide an accessible browser-based interface.
12. Deploy the application using Docker, GitHub, and Render.

---

## ✨ Key Features

### 1. AI-Powered Music Generation

- Integration of a trained MuseGAN model.
- Automatic generation of symbolic musical patterns.
- PyTorch-based model execution.
- Piano-roll-based musical representation.

### 2. Customizable Music Generation

Users can configure:

- Tempo.
- Music duration.
- Instrument selection.
- Genre.
- Mood.

### 3. Multi-Instrument Support

- 15 available General MIDI instrument choices.
- Multiple instrument tracks in generated MIDI compositions.
- Instrument-specific MIDI program assignments.
- SoundFont-based instrument rendering.

### 4. MIDI Generation

- Automatic MIDI creation.
- Multiple instrument tracks.
- Musical note and timing information.
- Instrument program assignments.
- Tempo information.

### 5. WAV Audio Generation

- MIDI-to-audio conversion.
- FluidSynth integration.
- General MIDI SoundFont support.
- Playable WAV output.
- Requested-duration adjustment.

### 6. Multi-Track Piano Roll Editor

- 88-pitch piano roll.
- 32 time steps.
- Up to 15 instrument tracks.
- Add and remove tracks.
- Add and remove notes.
- Clear track functionality.
- Tempo adjustment.
- Grid zoom.
- MIDI import and export.

### 7. Composition History

- Save generated composition information.
- Preserve genre metadata.
- Preserve mood metadata.
- Preserve selected instruments.

### 8. Online Deployment

- Flask-based web application.
- Docker containerization.
- Gunicorn production server.
- GitHub source-code management.
- Render cloud deployment.

---

## 🧠 AI Model - MuseGAN

Musegen AI uses MuseGAN, a generative adversarial network approach designed for symbolic multi-track music generation.

A Generative Adversarial Network (GAN) consists of two main components:

**Generator**

The generator produces synthetic musical patterns.

**Discriminator**

The discriminator attempts to distinguish between real musical examples and generated examples.

During GAN training, these networks compete with each other. The generator gradually learns to produce patterns resembling the musical characteristics of the training data.

### Model Integration

The project integrates an existing trained model checkpoint:

`musicforge_preferred_final_55_epochs.pth`

PyTorch is used to load and execute the trained model.

The project focuses on integrating the trained model into the application rather than retraining the model during the final application development.

### Model Output Representation

The model produces a three-dimensional piano-roll representation:

```python
(3, 88, 32)
```

| Dimension | Meaning |
|---|---|
| 3 | Original model-output tracks |
| 88 | Musical pitch positions |
| 32 | Musical time steps |

This representation is processed to identify active musical notes and construct MIDI compositions.

---

## ⚙️ Music Generation Process

The music-generation workflow consists of the following stages:

**Step 1: User Input**

The user selects tempo, duration, instruments, genre, and mood.

**Step 2: Frontend Request**

JavaScript collects the selected parameters and sends a request to the Flask backend.

**Step 3: Input Validation**

Flask validates the submitted generation settings.

The configured API limits include:

- Tempo: 60–180 BPM.
- Duration: 10–180 seconds.

**Step 4: Model Execution**

PyTorch loads and executes the trained MuseGAN checkpoint.

**Step 5: Pattern Generation**

The model produces a piano-roll tensor with the shape `(3, 88, 32)`.

**Step 6: Note Processing**

The generated numerical patterns are interpreted using a threshold to identify musical note events.

**Step 7: Instrument Assignment**

Generated patterns are distributed across the selected instrument tracks.

**Step 8: MIDI Creation**

Pretty MIDI constructs the MIDI composition with note pitches, timing, velocity, and instrument program information.

**Step 9: Audio Synthesis**

FluidSynth renders the MIDI using the installed General MIDI SoundFont.

**Step 10: Output Generation**

The application saves the MIDI and WAV files and makes the results available through the web interface.

### Music Generation Flow

```text
User Selects Music Parameters
             |
             v
      Music Studio UI
             |
             v
       Flask Backend
             |
             v
     PyTorch MuseGAN Model
             |
             v
      Piano Roll Output
        (3, 88, 32)
             |
             v
       Note Processing
             |
             v
     Instrument Assignment
             |
             v
        Pretty MIDI
             |
             v
          MIDI File
             |
             v
         FluidSynth
             |
             v
     General MIDI SoundFont
             |
             v
          WAV Audio
             |
             v
        User Playback
```

---

## 🎹 Supported Instruments

Musegen AI provides 15 instrument choices based on General MIDI programs.

| No. | Instrument | MIDI Program |
|---|---|---:|
| 1 | Piano | 0 |
| 2 | Bright Piano | 1 |
| 3 | Music Box | 10 |
| 4 | Guitar | 24 |
| 5 | Acoustic Guitar | 25 |
| 6 | Bass | 32 |
| 7 | Violin | 40 |
| 8 | Viola | 41 |
| 9 | Cello | 42 |
| 10 | Strings | 48 |
| 11 | Choir | 52 |
| 12 | Trumpet | 56 |
| 13 | Flute | 73 |
| 14 | Synth Lead | 80 |
| 15 | Synth Pad | 89 |

### How 15 Instrument Tracks Are Supported

The original MuseGAN model produces three output tracks.

To support more instrument selections, the application distributes the generated patterns across selected instrument tracks using a modulo-based mapping:

```python
piano_roll[track_index % 3]
```

This means the three original generated patterns are reused cyclically across the selected instrument tracks.

Each resulting MIDI track receives its own instrument program assignment.

For example:

- Piano can use the first generated pattern.
- Bright Piano can use the second generated pattern.
- Music Box can use the third generated pattern.
- Guitar can reuse the first generated pattern.
- Violin can also reuse the first generated pattern.

This allows the application to create MIDI arrangements containing up to 15 instrument tracks without changing the original model architecture.

**Technical note:** The additional tracks reuse the original three AI-generated patterns. They are not 12 additional independently generated AI tracks.

---

## 🎼 Genre and Mood Options

### Available Genres

- Classical
- Pop
- Jazz
- EDM
- Lo-fi

### Available Moods

- Happy
- Sad
- Romantic
- Energetic

These options are available through the Music Studio interface.

The current implementation stores genre as composition metadata and uses mood in the generation workflow to influence note velocity. The trained MuseGAN model has not been retrained with genre or mood labels, so these are not learned genre- or mood-conditioning inputs.

---

## 🎧 MIDI and WAV Audio Processing

Musegen AI generates two complementary output formats.

### MIDI

MIDI stands for Musical Instrument Digital Interface.

It stores musical instructions such as:

- Note pitch.
- Note start time.
- Note end time.
- Note velocity.
- Instrument program.
- Tempo.

MIDI is useful because it allows users to edit the musical composition.

### WAV

WAV is a digital audio format containing actual audio samples.

It can be played through compatible audio players and browsers.

### FluidSynth

FluidSynth is a software synthesizer that converts MIDI instructions into audio.

### SoundFont

The application uses the General MIDI SoundFont:

`FluidR3_GM.sf2`

The SoundFont provides sampled instrument sounds used by FluidSynth during rendering.

### Audio Generation Workflow

```text
Generated MIDI Composition
          |
          v
       FluidSynth
          |
          v
    General MIDI SoundFont
          |
          v
     Audio Synthesis
          |
          v
        WAV File
```

---

## 🎹 Piano Roll Editor

Musegen AI includes a multi-track Piano Roll Editor for visual MIDI editing.

### Editor Configuration

| Property | Supported Configuration |
|---|---|
| Maximum tracks | 15 |
| Pitch positions | 88 |
| Time steps | 32 |
| Tempo range | 30–300 BPM |
| MIDI import | Supported |
| MIDI export | Supported |

### Editor Features

**Add Instrument**

Users can add instrument tracks from the supported instrument list.

**Remove Track**

Users can remove an instrument track.

**Clear Track**

Users can remove the notes from an individual track.

**Add Notes**

Users can click on the piano-roll grid to add notes.

**Remove Notes**

Users can click existing notes to toggle them off.

**Tempo Adjustment**

Users can adjust the composition tempo using a slider.

**Grid Zoom**

Users can zoom the piano-roll grid for easier editing.

**MIDI Import**

Users can load existing MIDI compositions.

**MIDI Export**

Users can export their edited compositions as MIDI files.

**Browser Audio Preview**

The editor provides oscillator-based browser audio preview for checking note placement and timing. This preview is not the same as FluidSynth rendering with the original SoundFont samples.

---

## 🏗️ System Architecture

Musegen AI follows a frontend-backend architecture.

### Architecture Diagram

```text
                  USER
                   |
                   v
          WEB APPLICATION
           HTML / CSS / JS
                   |
                   v
             FLASK BACKEND
                app.py
                   |
        +----------+-----------+
        |          |           |
        v          v           v
   MUSIC         MIDI       CREATION
  GENERATOR      EDITOR      HISTORY
        |          |           |
        v          v           v
     PYTORCH    PRETTY MIDI   METADATA
     MUSEGAN        |
        |           |
        v           v
   PIANO-ROLL     MIDI FILE
     OUTPUT          |
                     v
                 FLUIDSYNTH
                     |
                     v
                  SOUNDFONT
                     |
                     v
                  WAV AUDIO
                     |
                     v
                 USER OUTPUT
```

### Component Responsibilities

| Component | Responsibility |
|---|---|
| Frontend | User interaction and displaying results |
| Flask | Backend routes and API communication |
| PyTorch | Trained model execution |
| MuseGAN | Symbolic music pattern generation |
| Music Generator | Processing patterns and preparing tracks |
| Pretty MIDI | MIDI creation and processing |
| MIDI Editor | Editing and exporting musical notes |
| FluidSynth | MIDI-to-audio synthesis |
| SoundFont | Instrument sound samples |
| Creation History | Saving composition metadata |

---

## 💻 Technology Stack

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| Google Colab | Development and testing environment |
| Google Drive | Project and model storage |
| PyTorch | AI model execution |
| MuseGAN | Symbolic music generation |
| Flask | Backend framework |
| HTML | Webpage structure |
| CSS | Interface styling |
| JavaScript | Frontend interactions |
| Pretty MIDI | MIDI processing |
| FluidSynth | Audio synthesis |
| FluidR3 GM SoundFont | General MIDI instrument sounds |
| NumPy | Numerical operations |
| SciPy | Scientific computing |
| SoundFile | Audio file handling |
| Gunicorn | Production application server |
| Docker | Application containerization |
| Git | Version control |
| GitHub | Source-code repository |
| Render | Cloud hosting |

---

## 📂 Project Structure

The following shows the main application files and their responsibilities.

```text
MusicForge_AI_MuseGAN/
│
├── app/
│   ├── app.py
│   │
│   ├── templates/
│   │   ├── studio.html
│   │   └── editor.html
│   │
│   ├── static/
│   │   └── js/
│   │       └── editor.js
│   │
│   └── utils/
│       ├── music_generator.py
│       ├── midi_editor.py
│       └── creation_history.py
│
├── checkpoints/
│   └── final/
│       └── musicforge_preferred_final_55_epochs.pth
│
├── requirements.txt
├── Dockerfile
├── render.yaml
└── README.md
```

### Important Files

| File | Description |
|---|---|
| `app.py` | Flask application and API routes |
| `music_generator.py` | AI music generation and audio processing |
| `midi_editor.py` | MIDI editing and processing |
| `creation_history.py` | Composition history and metadata |
| `studio.html` | Music Studio interface |
| `editor.html` | Piano Roll Editor interface |
| `editor.js` | Interactive editor functionality |
| `requirements.txt` | Python dependencies |
| `Dockerfile` | Docker environment configuration |
| `render.yaml` | Render deployment configuration |
| Model checkpoint | Trained MuseGAN model weights |

---

## 🚀 Installation and Setup

### 1. Clone the Repository

```bash
git clone https://github.com/likithareddy38/Musegen-AI.git
cd Musegen-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

Activate it:

**Windows:**

```bash
venv\Scripts\activate
```

**Linux/macOS:**

```bash
source venv/bin/activate
```

### 3. Install Python Dependencies

```bash
pip install -r requirements.txt
```

The project uses a CPU-only PyTorch dependency for its CPU-based Render deployment:

```text
--extra-index-url https://download.pytorch.org/whl/cpu
torch==2.11.0+cpu
```

### 4. Install FluidSynth and SoundFont

The application requires FluidSynth and a General MIDI SoundFont for MIDI-to-WAV rendering.

**Ubuntu/Debian:**

```bash
sudo apt-get update

sudo apt-get install -y \
    libfluidsynth3 \
    fluid-soundfont-gm
```

### 5. Verify SoundFont Availability

The expected SoundFont location in the development and deployment environments is:

```text
/usr/share/sounds/sf2/FluidR3_GM.sf2
```

The generator must be configured to use the SoundFont path available in its runtime environment.

### 6. Model Checkpoint

Ensure that the trained checkpoint is available at:

```text
checkpoints/final/musicforge_preferred_final_55_epochs.pth
```

The checkpoint is required for AI music generation.

If it is not included in the cloned repository, place the trained model file in the expected directory before running generation.

---

## ▶️ Running the Application

From the project root, start the Flask application using:

```bash
python -m flask --app app.app run --host=0.0.0.0 --port=5000
```

Alternatively, if the Flask module is configured to start the application directly:

```bash
python app/app.py
```

Open the following address in your browser:

```text
http://localhost:5000
```

The application can then be used to access the Music Studio and Piano Roll Editor.

---

## 🔌 API Overview

The Flask backend provides the music-generation API.

### Music Generation

**Endpoint:**

```text
POST /api/generate
```

The frontend sends the selected generation settings to this endpoint.

The request includes parameters such as:

```json
{
  "tempo": 120,
  "duration": 30,
  "threshold": 0.5,
  "instruments": ["Piano", "Violin"],
  "genre": "Classical",
  "mood": "Happy"
}
```

The backend validates the request and invokes the music-generation module.

The generated result is returned to the frontend.

The actual response structure depends on the Flask implementation.

### Input Validation

The generation API validates:

- Tempo.
- Duration.
- Instrument selection.
- Request parameters.

Configured limits include 60–180 BPM and 10–180 seconds.

---

## 🐳 Docker Configuration

Docker is used to package the application and its dependencies into a container.

The application requires both Python packages and operating-system-level audio dependencies.

The Dockerfile uses Python 3.11 slim and installs FluidSynth and the General MIDI SoundFont.

### Main Dockerfile

```dockerfile
FROM python:3.11-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    libfluidsynth3 \
    fluid-soundfont-gm \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD gunicorn --bind 0.0.0.0:${PORT:-10000} --workers 1 --threads 4 --timeout 300 app.app:app
```

### Build the Docker Image

```bash
docker build -t musegen-ai .
```

### Run the Container

```bash
docker run -p 10000:10000 musegen-ai
```

The application can then be accessed through the configured local port.

---

## ☁️ Deployment on Render

Musegen AI is deployed using Render.

### Deployment Process

1. Push the project source code to GitHub.
2. Open Render.
3. Create a new Web Service.
4. Connect the GitHub repository.
5. Select the Docker deployment environment.
6. Configure the service.
7. Allow Render to build the Docker image.
8. Install the Python and system dependencies.
9. Start the Flask application through Gunicorn.
10. Verify the deployment health check.
11. Open the public application URL.

### Deployment Configuration

The project uses:

- Docker runtime.
- Python 3.11.
- Gunicorn.
- FluidSynth.
- General MIDI SoundFont.
- Health check path `/`.

### Live Application

https://musegen-ai.onrender.com

---

## 🧪 Testing and Validation

Testing was performed during development and after deployment.

### Model Testing

- Verified model checkpoint loading.
- Tested PyTorch model execution.
- Checked the generated piano-roll dimensions.
- Verified note-processing functionality.

### MIDI Testing

- Tested MIDI creation.
- Checked instrument assignments.
- Verified track counts.
- Checked tempo and note information.
- Tested MIDI export.

### Audio Testing

- Verified FluidSynth availability.
- Installed and checked the SoundFont.
- Tested MIDI-to-WAV rendering.
- Checked generated audio duration.

### Multi-Instrument Testing

- Tested generation with multiple selected instruments.
- Verified a six-instrument local generation.
- Tested instrument-track creation.
- Tested multi-instrument generation on the deployed application.

### Editor Testing

- Tested adding and removing tracks.
- Tested adding and removing notes.
- Tested tempo adjustment.
- Tested MIDI import and export.

### Deployment Testing

- Verified the online application.
- Tested the generation API.
- Investigated production errors.
- Confirmed that multi-instrument generation beyond four instruments was working after the deployment fixes.

---

## 🛠️ Challenges and Solutions

### 1. Integrating the Trained AI Model

**Challenge:** The trained model needed to be integrated into a web application.

**Solution:** Integrated the existing MuseGAN checkpoint using PyTorch and implemented the generation workflow in Python.

### 2. Converting Musical Patterns into MIDI

**Challenge:** The model produces numerical piano-roll patterns rather than finished audio.

**Solution:** Used note-processing logic and Pretty MIDI to construct musical tracks.

### 3. Generating Actual Audio

**Challenge:** MIDI contains musical instructions, not recorded instrument audio.

**Solution:** Integrated FluidSynth and the General MIDI SoundFont to render MIDI into WAV.

### 4. Supporting More Than Three Model Tracks

**Challenge:** The original model output contains three tracks, while the application needed up to 15 instrument tracks.

**Solution:** Implemented modulo-based pattern distribution across selected instrument tracks.

### 5. Accurate Audio Duration

**Challenge:** The rendered audio needed to match the requested duration.

**Solution:** Implemented trimming and padding of the generated WAV audio.

### 6. Missing SoundFont in Deployment

**Challenge:** The production container required the audio synthesis library and SoundFont.

**Solution:** Updated the Dockerfile to install `libfluidsynth3` and `fluid-soundfont-gm`.

### 7. Multi-Instrument HTTP 502 Error

**Challenge:** Music generation worked with four instruments, but requests with more instruments returned HTTP 502 on Render.

**Investigation:** Examined deployment logs, Flask behavior, frontend response parsing, and the PyTorch dependency configuration. The Render environment had resolved an unpinned PyTorch dependency to a CUDA-enabled build despite running on CPU.

**Solution:** Pinned PyTorch to a CPU-only build and improved frontend handling of empty or non-JSON server responses. The CPU optimization addressed unnecessary GPU-related dependencies, although it was not independently proven to be the sole cause of every 502 response.

**Result:** The updated application was deployed and multi-instrument generation beyond four instruments was successfully tested.

---

## ⚠️ Current Implementation Details and Limitations

The following details describe the current implementation accurately:

- The trained MuseGAN model produces three original musical output tracks.
- Up to 15 MIDI instrument tracks are supported by distributing and reusing those three generated patterns.
- Genre is stored as metadata and is not currently a learned model-conditioning input.
- Mood influences note velocity in the generation workflow; the model has not been retrained with mood labels.
- The Piano Roll Editor supports click-to-toggle note editing.
- Advanced note dragging, resizing, and velocity editing are not currently implemented.
- The editor's browser preview uses oscillator-based audio rather than the original SoundFont instrument samples.
- MIDI and WAV generation are separate stages of the output workflow.

---

## 🔮 Future Enhancements

Possible future improvements include:

1. Training or fine-tuning a genre-conditioned music generation model.
2. Introducing learned mood-conditioned music generation.
3. Generating longer and more complex musical compositions.
4. Improving melody and harmony consistency.
5. Supporting more independently generated instrument tracks.
6. Adding note dragging and resizing.
7. Adding note velocity editing.
8. Adding undo and redo functionality.
9. Integrating SoundFont-based playback directly into the editor.
10. Adding user authentication.
11. Providing cloud-based composition storage.
12. Allowing users to share compositions.
13. Supporting additional export formats.
14. Improving audio rendering and performance.

---

## 👥 Team Contributions

The project can be divided into the following five responsibility areas. The actual assignments should reflect the work completed by each team member.

| Team Member | Responsibility | Contribution |
|---|---|---|
| Member 1 | AI Model Development | MuseGAN architecture study, checkpoint integration and PyTorch execution. |
| Member 2 | Music Generation | Generation logic, instrument selection, tempo and duration controls, MIDI generation. |
| Member 3 | Backend Development | Flask routes, API integration, input validation, file handling and composition history. |
| Member 4 | Frontend and MIDI Editor | Music Studio interface, Piano Roll Editor, JavaScript interactions and MIDI import/export. |
| Member 5 | Audio Processing and Deployment | FluidSynth, SoundFont, audio testing, Docker, GitHub, Render and deployment troubleshooting. |

---

## 🙏 Acknowledgements

We acknowledge the developers and researchers behind MuseGAN and the open-source technologies used in this project.

We also acknowledge the communities and maintainers of PyTorch, Flask, Pretty MIDI, FluidSynth, and other supporting libraries.

These technologies made it possible to integrate AI-based music generation, MIDI processing, audio synthesis, and web application development into a single platform.

---

## 📜 License

A license has not yet been specified for this repository.

Before distributing the project, add an appropriate license and verify the licensing conditions of the trained model checkpoint, training data, and SoundFont assets.

---

## ⭐ Final Note

Musegen AI demonstrates how artificial intelligence, symbolic music generation, MIDI processing, audio synthesis, and web technologies can be combined to create an accessible music-generation platform.

The project integrates an existing trained MuseGAN model with a browser-based Music Studio and multi-track Piano Roll Editor, and is deployed online using Docker and Render.

**Developed as an AI-powered music generation and editing application.**

🌐 Live: https://musegen-ai.onrender.com

💻 Source: https://github.com/likithareddy38/Musegen-AI
