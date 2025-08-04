import time
import mss                    # For fast screen capture
import numpy as np            # For image array processing
import pyautogui              # For simulating keyboard presses
import json                   # For saving the bot's memory to a file

# This list will store everything the bot remembers during runtime
memory = []

# Function to take a screenshot of the screen or a specific region
def screen_capture(region=None):
    with mss.mss() as sct:
        monitor = region if region else sct.monitors[1]  # Default to primary monitor
        img = np.array(sct.grab(monitor))  # Capture and convert to NumPy array
        return img

# Function to check if any red pixels are visible in the screenshot
def see_red(img):
    # A "red pixel" here means:
    # - Red channel > 200
    # - Green channel < 100
    # - Blue channel < 100
    red_pixels = (img[:, :, 0] > 200) & (img[:, :, 1] < 100) & (img[:, :, 2] < 100)
    return np.any(red_pixels)  # Return True if any such pixels exist

# Function to press a key using pyautogui
def press_key(key):
    pyautogui.press(key)

# Function to store an event in memory
def log_memory(event_type, data):
    memory.append({
        'time': time.time(),  # Current timestamp
        'type': event_type,   # Could be 'observation' or 'action'
        'data': data          # Details of what happened
    })

# Function to save the memory list to a JSON file
def save_memory():
    with open('bot_memory.json', 'w') as f:
        json.dump(memory, f, indent=2)

# ----------- MAIN LOOP ----------- #
try:
    while True:
        img = screen_capture()            # Take a screenshot
        if see_red(img):                  # If red is detected
            press_key('a')                # Press the "A" key
            log_memory('action', {        # Log that the bot took an action
                'saw': 'red',
                'did': 'press_a'
            })
        else:
            log_memory('observation', {   # Log that it didn't see red
                'saw': 'no_red'
            })

        time.sleep(0.2)  # Delay to control speed (200ms loop)
except KeyboardInterrupt:
    # When the user stops the script (Ctrl+C), save what the bot remembers
    save_memory()
    print("Saved memory and stopped.")
