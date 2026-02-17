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
        json.dump(example_data, f, indent=2)
    
    print(f"✓ Created example {json_path}")
    return json_path


def main():
    """Batch processing example."""
    # Create example JSON if it doesn't exist
    json_file = Path("titles.json")
    if not json_file.exists():
        create_example_json()
    
    # Initialize client
    client = GeminiClient(
        headless=False,
        output_dir="generated_images"
    )
    
    try:
        # Process batch
        print("Starting batch processing...")
        logo_path = "logo.png" if Path("logo.png").exists() else None
        
        images = client.process_batch(
            json_file=str(json_file),
            logo_path=logo_path
        )
        
        print(f"\n✓ Batch processing complete!")
        print(f"Generated {len(images)} images:")
        for img_path in images:
            print(f"  - {img_path}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
