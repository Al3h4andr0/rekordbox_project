import os
import shutil
import pandas as pd
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TKEY, TBPM, TCON
import librosa
import json

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

    # def save_metadata(self):
    #     """Saves extracted metadata to a JSON file."""
    #     with open(self.metadata_file, "w", encoding="utf-8") as f:
    #         json.dump(self.tracks, f, indent=4)
    
    # def extract_metadata(self, file_path):
    #     """Extracts metadata from an audio file using mutagen."""
    #     try:
    #         audio = MP3(file_path, ID3=ID3)
    #         tags = audio.tags
            
    #         title = tags.get("TIT2", TIT2(encoding=3, text=os.path.basename(file_path))).text[0]
    #         key = tags.get("TKEY", TKEY(encoding=3, text="Unknown")).text[0]
    #         bpm_tag = tags.get("TBPM")
    #         bpm = float(bpm_tag.text[0]) if bpm_tag and bpm_tag.text[0] == float(bpm_tag.text[0]) else None

    #         # # If BPM is missing, calculate it using librosa
    #         if bpm is None or bpm == 0:
    #             y, sr = librosa.load(file_path, sr=22050)
    #             tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    #             bpm = round(float(tempo[0])) if tempo.size > 0 else 0

    #         return {
    #             'Title': title,
    #             'BPM': float(bpm) if bpm == float(bpm) else 0,
    #             # 'Key': self.convert_key(key),
    #             'Key': key,
    #             'Filepath': file_path
    #         }
    #     except Exception as e:
    #         print(f"Error extracting metadata from {file_path}: {e}")
    #         return None
        
    # def find_music_files(self):
    #     """Recursively searches for music files and extracts metadata only if missing."""
    #     existing_files = {track['Filepath'] for track in self.tracks}
    #     new_tracks = []
        
    #     for root, _, files in os.walk(self.music_folder):
    #         for file in files:
    #             if file.endswith(".mp3"):
    #                 file_path = os.path.join(root, file)
    #                 if file_path not in existing_files:
    #                     metadata = self.extract_metadata(file_path)
    #                     if metadata:
    #                         new_tracks.append(metadata)
        
    #     if new_tracks:
    #         self.tracks.extend(new_tracks)
    #         self.save_metadata()
    
    # def convert_key(self, key):
    #     """Converts between Camelot and Classical notation."""
    #     return camelot_to_classical.get(key, key)  # Default to original key if no match

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

# Example usage
music_folder = "C:\\Users\\ioan_\\Music\\"
output_folder = "C:\\Users\\ioan_\\Music\\RekordboxRecommendations"
metadata_file = "C:\\Users\\ioan_\\Music\\rekordbox_metadata.json"

plugin = RekordboxPlaylistAnalyzer(music_folder, output_folder, metadata_file)
current_track = {"Title": "Alan Fitzpatrick - We Do What We Want (Full Track)", "BPM": 123, "Key": "4A"}
recommendations = plugin.run(current_track)
print("Recommended Tracks:", [song['Title'] for song in recommendations])