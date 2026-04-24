import os
import json
from resolve_file import resolve_filename


# --- Save Dashboard to JSON ---
def save_dashboard(data, filename="VisualData/dashboard.json"):
    """
    Saves the dashboard data dict to a JSON file.
    Respects the user's file-conflict choice from resolve_filename.
    Does nothing (with a message) if the user cancels.
    """
    resolved = resolve_filename(filename)

    if resolved is None:          # user chose Cancel
        print("Dashboard JSON save cancelled.")
        return

    os.makedirs(os.path.dirname(resolved), exist_ok=True)

    try:
        with open(resolved, "w") as f:
            json.dump(data, f, indent=4)
        print(f"\nDashboard saved → {resolved}")

    except Exception as e:
        print(f"Error saving JSON: {e}")