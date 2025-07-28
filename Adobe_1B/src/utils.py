import json
from datetime import datetime
from typing import Any, Dict

# Load input JSON file safely
def load_input_json(file_path: str) -> Dict[str, Any]:
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {file_path}: {e}")
        return {}

# Save output data to JSON file
def save_output_json(data: Dict[str, Any], file_path: str) -> None:
    try:
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
    except Exception as e:
        print(f"Error saving {file_path}: {e}")

# Get current timestamp in ISO format
def get_timestamp() -> str:
    return datetime.now().isoformat()