import os
import shutil
import pandas as pd
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TKEY, TBPM, TCON
import librosa
import json
import pytesseract


def load_metadata():
        """Loads metadata from the saved file if available, else returns an empty list."""
        if os.path.exists(metadata_file):
            with open(metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

camelot_to_classical = {
    "1A": "Abm", "1B": "B",
    "2A": "Ebm", "2B": "F#",
    "3A": "Bbm", "3B": "Db",
    "4A": "Fm", "4B": "Ab",
    "5A": "Cm", "5B": "Eb",
    "6A": "Gm", "6B": "Bb",
    "7A": "Dm", "7B": "F",
    "8A": "Am", "8B": "C",
    "9A": "Em", "9B": "G",
    "10A": "Bm", "10B": "D",
    "11A": "F#m", "11B": "A",
    "12A": "Dbm", "12B": "E"
}
music_folder = "C:\\Users\\ioan_\\Music\\"
output_folder = "C:\\Users\\ioan_\\Music\\RekordboxRecommendations"
metadata_file = "C:\\Users\\ioan_\\Music\\rekordbox_metadata.json"
tracks = load_metadata()


def save_metadata():
        """Saves extracted metadata to a JSON file."""
        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(tracks, f, indent=4)
    
def extract_metadata(file_path):
    """Extracts metadata from an audio file using mutagen."""
    try:
        audio = MP3(file_path, ID3=ID3)
        tags = audio.tags
        
        title = tags.get("TIT2", TIT2(encoding=3, text=os.path.basename(file_path))).text[0]
        key = tags.get("TKEY", TKEY(encoding=3, text="Unknown")).text[0]
        bpm_tag = tags.get("TBPM")
        bpm = float(bpm_tag.text[0]) if bpm_tag and bpm_tag.text[0] == float(bpm_tag.text[0]) else None

        # # If BPM is missing, calculate it using librosa
        if bpm is None or bpm == 0:
            y, sr = librosa.load(file_path, sr=22050)
            tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
            bpm = round(float(tempo[0])) if tempo.size > 0 else 0

        return {
            'Title': title,
            'BPM': float(bpm) if bpm == float(bpm) else 0,
            'Key': key,
            'Filepath': file_path
        }
    except Exception as e:
        print(f"Error extracting metadata from {file_path}: {e}")
        return None
    
def find_music_files():
    """Recursively searches for music files and extracts metadata only if missing."""
    existing_files = {track['Filepath'] for track in tracks}
    new_tracks = []
    
    for root, _, files in os.walk(music_folder):
        for file in files:
            if file.endswith(".mp3"):
                file_path = os.path.join(root, file)
                if file_path not in existing_files:
                    metadata = extract_metadata(file_path)
                    if metadata:
                        new_tracks.append(metadata)
                        print(f'New Track found: {metadata}')
    
    if new_tracks:
        tracks.extend(new_tracks)
        save_metadata()

def convert_key(key):
    """Converts between Camelot and Classical notation."""
    return camelot_to_classical.get(key, key)  # Default to original key if no match


def main():
    find_music_files()


if __name__ == "__main__":
    main()
