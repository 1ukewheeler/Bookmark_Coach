import subprocess
import time
import requests
import json
import sys

def get_active_app():
    # Gets the active app name using Apple Script
    script = 'tell application "System Events" to get name of first process whose frontmost is true'
    try:
        # Runs the script, returns the active app name as a string
        return subprocess.check_output(['osascript', '-e', script]).decode('utf-8').strip()
    except:
        # If the script didn't run for some reason, returns "Unknown"
        return "Unknown"







# --- Main Loop ---
print("--- Starting AI Workflow Coach ---")
last_app = ""

while True:
    current_app = get_active_app()
    
    # Only trigger AI if the app changed (to save resources)
    if current_app != last_app:
        print(f"\n[Activity] Switched to: {current_app}")
        last_app = current_app
        
    time.sleep(1) # Check every 5 seconds