import json
import os

class ShortcutManager:
    def __init__(self, data_dir="shortcuts_data"):
        self.data_dir = data_dir
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)

    def _get_path(self, app_name):
        return os.path.join(self.data_dir, f"{app_name}.json")

    def load_shortcuts(self, app_name):
        path = self._get_path(app_name)
        if not os.path.exists(path):
            return {}
        
        with open(path, 'r') as f:
            data = json.load(f)
        
        # LOGIC: Delete unstarred shortcuts on load (as requested)
        cleaned_data = {k: v for k, v in data.items() if v.get('starred', False)}
        return cleaned_data

    def save_shortcuts(self, app_name, shortcuts):
        path = self._get_path(app_name)
        with open(path, 'w') as f:
            json.dump(shortcuts, f, indent=4)

    def get_sorted_list(self, shortcuts):
        # LOGIC: Starred shortcuts on top
        return sorted(shortcuts.items(), key=lambda x: x[1]['starred'], reverse=True)

# Example Usage
manager = ShortcutManager()
app = "Firefox"
my_shortcuts = manager.load_shortcuts(app)

# Add a new one from AI
my_shortcuts["Cmd+L"] = {"desc": "Focus address bar", "starred": False}
manager.save_shortcuts(app, my_shortcuts)