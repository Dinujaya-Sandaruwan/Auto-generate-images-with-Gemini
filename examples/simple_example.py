"""Simple example of using Gemini Automation."""

from gemini_automation import GeminiClient


def main():
    """Simple example: generate a single image."""
    # Initialize client
    client = GeminiClient(
        headless=False,  # Set to True to run without browser window
        output_dir="generated_images"
    )
    
    try:
        # Generate an image
        print("Generating image...")
        image_path = client.generate_image(
            prompt="A beautiful sunset over mountains with a lake",
            title="sunset_mountains"
        )
        
        print(f"✓ Success! Image saved to: {image_path}")
        
    except Exception as e:
        print(f"✗ Error: {e}")
    finally:
        client.close()


if __name__ == "__main__":
    main()
