"""Example of batch processing with Gemini Automation."""

import json
from pathlib import Path
from gemini_automation import GeminiClient


def create_example_json():
    """Create an example titles.json file."""
    example_data = {
        "titles": [
            "How to Build a Website",
            "Python Programming Tips",
            "Machine Learning Basics",
            "Web Development Guide",
            "Data Science Tutorial"
        ]
    }
    
    json_path = Path("titles.json")
    with open(json_path, 'w', encoding='utf-8') as f: