# 🎧 Rekordbox Live Track Recommender

A real-time song recommendation plugin for Rekordbox DJs.
This Python-based tool extracts the currently playing track’s metadata (Title, BPM, Key) directly from the Rekordbox UI using OCR, then suggests harmonically compatible tracks from your local library and generates a ready-to-import Rekordbox XML playlist.

🚀 Features

    🧠 Live Song Detection from Deck 1 or 2 (user-selectable)

    🔎 OCR-Based Metadata Extraction (Title, BPM, Key)

    🎼 Harmonic Mixing Suggestions using Camelot wheel logic

    🗂 Auto-Generated Rekordbox Playlist via XML

    ⚡ One-Hotkey Workflow (Ctrl+Alt+R) or CLI-triggered

    📁 Offline Metadata Preprocessing for large libraries

    🎛️ Future-ready for GUI / tray icon interaction

🧰 Technologies Used

    Python (3.9+)

    PyAutoGUI – screen capture

    OpenCV – image preprocessing

    Tesseract OCR – text recognition

    mutagen, librosa – audio metadata and BPM extraction

    xml.etree.ElementTree – Rekordbox XML generation

    keyboard – global hotkey integration

🛠️ Setup

    Install dependencies:

  <bash> ```pip install -r requirements.txt``` </bash>

    Install Tesseract:

  [Windows](https://github.com/UB-Mannheim/tesseract/wiki)

    Add the installation path to your code (pytesseract.pytesseract.tesseract_cmd)

    Edit paths (optional):

    Set your music_folder, metadata_file, and output_folder in launcher.py.

▶️ Usage

    Preprocess your music library (only once):

<bash> ```python save_metadata.py``` </bash>

    Run the plugin:

<bash> ```python launcher.py```</bash>

    In the terminal:

    Choose the deck to analyze (1 or 2)

    In Rekordbox:

    Go to Preferences → Advanced → Rekordbox XML

    Load: rekordbox_plugin_playlist.xml

    Import the generated playlist: Live Suggestions

📸 Screenshot

TBD :D 

🧠 How It Works

    OCR reads the UI region of the selected deck (screen coordinates are scalable).

    Text is parsed to get the track title, BPM, and Camelot key.

    Matching tracks are pulled from the JSON metadata file based on harmonic mixing rules.

    XML is generated and made ready for live import into Rekordbox.

✅ To Do (Coming Soon)

GUI Interface (Tkinter or PyQt)

System Tray Icon + Quick Actions

Confidence Scoring for OCR

Drag-and-drop support for folders

    Audio fingerprinting for song matching (no metadata)

💬 Example Output

Currently playing: Lose Yourself
BPM: 87
Key: 6A

Recommended Tracks:
- NF - Let You Down
- Logic - 44 More
- Hopsin - Ill Mind of Hopsin 5


🧠 Motivation

Created for live B2B DJ performances where track selection must be quick, harmonic, and seamless. Designed to work without restarting Rekordbox or interfering with performance. 
