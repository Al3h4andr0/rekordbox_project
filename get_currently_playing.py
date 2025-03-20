import pyautogui
import pytesseract
import cv2
import time
import os
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"

import pyautogui
import pytesseract
import cv2
import time
import os

# Get screen resolution dynamically
SCREEN_WIDTH, SCREEN_HEIGHT = pyautogui.size()

# Define the region as a percentage of screen size (Adjust as needed)
REGION_X = int(SCREEN_WIDTH * 0.02)  # 10% from the left
REGION_Y = int(SCREEN_HEIGHT * 0.28)  # 20% from the top
REGION_WIDTH = int(SCREEN_WIDTH * 0.25)  # 30% of screen width
REGION_HEIGHT = int(SCREEN_HEIGHT * 0.048)  # 10% of screen height

# Scalable Screenshot Region
SCREENSHOT_REGION = (REGION_X, REGION_Y, REGION_WIDTH, REGION_HEIGHT)

def capture_screenshot():
    """Captures a screenshot of the specified region."""
    screenshot = pyautogui.screenshot(region=SCREENSHOT_REGION)
    screenshot.save("rekordbox_screen.png")
    return "rekordbox_screen.png"

def process_image(image_path):
    """Processes the screenshot and extracts text."""
    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # Convert to grayscale
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)  # Improve contrast
    text = pytesseract.image_to_string(thresh)
    print("------------")
    print(text)
    print("------------")
    return text

def extract_info(text):
    """Extracts song name, BPM, and key from OCR output."""
    lines = text.split("\n")
    song_name = lines[0]
    bpm = lines[1].split()[0]
    key = lines[1].split()[1][:-1]

    return song_name, bpm, key

def save_to_txt(song_name, bpm, key):
    if int(key[-1]) == 4:
        key = key[:-1] + 'A'
    """Saves extracted information to a text file."""
    with open("rekordbox_info.txt", "w") as file:
        file.write(f"{song_name}||{bpm}||{key}")

def main():
    """Runs the automation to extract song details."""
    print(f"Screen Size: {SCREEN_WIDTH}x{SCREEN_HEIGHT}")
    print(f"Capturing Screenshot at: {SCREENSHOT_REGION}")

    image_path = capture_screenshot()

    print("Processing OCR...")
    extracted_text = process_image(image_path)

    print("Extracting information...")
    song_name, bpm, key = extract_info(extracted_text)

    print("Saving to file...")
    save_to_txt(song_name, bpm, key)
    
    print("Extraction Complete!")
    print(f"Song: {song_name}, BPM: {bpm}, Key: {key}")

if __name__ == "__main__":
    main()
