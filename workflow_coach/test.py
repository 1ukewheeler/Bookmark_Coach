import subprocess
import time
import requests
import json
import sys

def ensure_ollama_is_running():
    """Checks if Ollama is responsive; if not, tries to start it."""
    try:
        # Check if the Ollama server is responding
        requests.get("http://localhost:11434/api/tags")
        print ("Checking Ollama server")
    except:
        print("[System] Ollama not detected. Starting server...")
        # Start the Ollama serve process in the background
        subprocess.Popen(["ollama", "serve"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(5) # Give it time to boot

def get_active_app():
    # Gets the active app name using Apple Script
    script = 'tell application "System Events" to get name of first process whose frontmost is true'
    try:
        # Runs the script, returns the active app name as a string
        return subprocess.check_output(['osascript', '-e', script]).decode('utf-8').strip()
    except:
        # If the script didn't run for some reason, returns "Unknown"
        return "Unknown"

def pull_and_set_model():
    global current_model
    url_pull = "http://localhost:11434/api/pull"
    
    # 1. Ask for the name of the new model
    new_model_name = input("\nEnter the name of the model to download (e.g., 'phi3', 'mistral'): ").strip()
    
    if not new_model_name:
        print("No name entered. Aborting.")
        return

    print(f"--- Initializing download for '{new_model_name}' ---")
    
    try:
        # 2. Download the model with a live status indicator
        # We use stream=True so we can read the progress as it happens
        response = requests.post(url_pull, json={"name": new_model_name}, stream=True)
        
        for line in response.iter_lines():
            if line:
                # Parse the status from the JSON chunk sent by Ollama
                data = json.loads(line)
                status = data.get('status', 'processing...')
                
                # The \r (carriage return) lets us overwrite the same line in the terminal
                sys.stdout.write(f"\r[Ollama] {status}... ")
                sys.stdout.flush()

        # 3. Set the newly downloaded model as the current_model
        current_model = new_model_name
        print(f"\n[Success] '{current_model}' is now active and ready for use.")

    except Exception as e:
        print(f"\n[Error] Failed to download model: {e}")

def change_model():
    global current_model
    url = "http://localhost:11434/api/tags"
    
    try:
        # 1. Fetch the current list of installed models
        response = requests.get(url)
        models_data = response.json().get('models', [])
        # We strip the ':latest' tag often added by Ollama for a cleaner display
        model_names = [m['name'] for m in models_data]
        
        print("\n--- Model Management ---")
        print("1. [Download & Install a New Model]")
        for i, name in enumerate(model_names, start=2):
            print(f"{i}. {name}")
            
        choice = input("\nSelect an option: ")
        
        if choice == "1":
            # Jump to your specialized download function
            pull_and_set_model()
        else:
            try:
                idx = int(choice) - 2
                if 0 <= idx < len(model_names):
                    current_model = model_names[idx]
                    print(f"[System] Switched to: {current_model}")
                else:
                    print("[Alert] Invalid selection. No changes made.")
            except ValueError:
                print("[Alert] Please enter a valid number.")
                
    except Exception as e:
        print(f"Network error: {e}")

def get_ai_advice(app_name):
    # Sends the current app to local Ollama instance for feedback
    url = "http://localhost:11434/api/generate"
    
    # This is the 'Metacognitive' prompt
    prompt = f"""
    The user is an Engineering Physics student. 
    Current active app: {app_name}.
    Context: They have a Fluid Mechanics project and a CAD assignment due soon.
    Task: Give a 1-sentence, witty, and helpful critique of their current focus.
    """
    
    payload = {
        "model": current_model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload)
        return response.json().get('response', 'No advice available.')
    except:
        return "Error: Is Ollama running?"

# --- Main Loop ---
print("--- Starting AI Workflow Coach ---")
change_model()
ensure_ollama_is_running()
last_app = ""

while True:
    current_app = get_active_app()
    
    # Only trigger AI if the app changed (to save resources)
    if current_app != last_app:
        print(f"\n[Activity] Switched to: {current_app}")
        advice = get_ai_advice(current_app)
        print(f"[Coach] {advice}")
        last_app = current_app
        
    time.sleep(5) # Check every 5 seconds