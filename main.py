import os
import shutil
import pandas as pd
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TKEY, TBPM, TCON
import librosa
import json
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

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

class RekordboxPlaylistAnalyzer:
    def __init__(self, music_folder, output_folder, metadata_file="metadata.json"):
        self.music_folder = music_folder
        self.output_folder = output_folder
        self.metadata_file = metadata_file
        self.tracks = self.load_metadata()
    
    def load_metadata(self):
        """Loads metadata from the saved file if available, else returns an empty list."""
        if os.path.exists(self.metadata_file):
            with open(self.metadata_file, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def find_recommendations(self, current_track):
        """Finds songs compatible with the current track based on BPM and Key."""
        bpm_range = (current_track['BPM'] * 0.85, current_track['BPM'] * 1.15)  # ±15% BPM range
        compatible_keys = self.get_compatible_keys(current_track['Key'])
        print(compatible_keys)
        return [track for track in self.tracks 
                if bpm_range[0] <= track['BPM'] <= bpm_range[1] and track['Key'] in compatible_keys and track['Title'].strip('.mp3') != current_track['Title'].strip('.mp3')]
    
    def get_compatible_keys(self, key):
        """Returns a list of compatible keys for harmonic mixing."""
        camelot_keys = list(camelot_to_classical.keys())
        classical_keys = list(camelot_to_classical.values())
        compatible_keys = set()
        if key in camelot_keys:
            number = key[:-1]
            letter = key[-1]
            print(number)
            print(letter)
            if int(number) != 1:
                compatible_keys = {f'{(int(number)-1)%12}{letter}'}
                print('diferit de 1')
                print(compatible_keys)
            if int(number) == 1:
                compatible_keys = {f'12{letter}'}
            print(compatible_keys)
            print(f'{(int(number)+1)%12}{letter}', f'{int(number)}A', f'{int(number)}B')
            compatible_keys.add(f'{(int(number)+1)%12}{letter}')
            compatible_keys.add(f'{int(number)}A')
            compatible_keys.add(f'{int(number)}B')
        return compatible_keys if compatible_keys else {key}  # Default to same key if not found in Camelot system

    def create_recommendation_folder(self, recommended_tracks):
        """Creates a new folder with recommended tracks."""
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
        for track in recommended_tracks:
            source = track['Filepath']
            destination = os.path.join(self.output_folder, os.path.basename(source))
            if os.path.exists(source):
                shutil.copyfile(source, destination)
            
    def run(self, current_track):
        # self.find_music_files()
        recommendations = self.find_recommendations(current_track)
        self.create_recommendation_folder(recommendations)
        return recommendations

def get_current_track():
    track = {}
    with open('rekordbox_info.txt', 'r', encoding='utf-8') as lines:
        for line in lines:
            info = line.split('||')
            print(info)
        track['Title'] = info[0]
        track['BPM'] = float(info[1])
        track['Key'] = info[2]
        print('---------')
        print(info)
        print('---------')
    return track


# Example usage
music_folder = "C:\\Users\\ioan_\\Music\\"
output_folder = "C:\\Users\\ioan_\\Music\\RekordboxRecommendations"
metadata_file = "C:\\Users\\ioan_\\Music\\rekordbox_metadata.json"

plugin = RekordboxPlaylistAnalyzer(music_folder, output_folder, metadata_file)
current_track = get_current_track()
recommendations = plugin.run(current_track)
print("Recommended Tracks:", [song['Title'] for song in recommendations])