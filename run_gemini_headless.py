import time
import os
from gemini_automation import GeminiClient

def main():
    print("--- Generating Image using Headless Browser ---")
    headless_client = GeminiClient(headless=True, wait_timeout=120)
    try:
        headless_client.initialize()
        prompt = "A majestic cyberpunk cityscape at sunset, neon lights reflecting on wet streets, high quality, highly detailed 8k"
        print(f"Generating image with prompt: '{prompt}'...")
        image_path = headless_client.generate_image(prompt=prompt, title="cyberpunk_city")
        print(f"Success! Image saved to: {os.path.abspath(image_path)}")
    except Exception as e:
        print(f"Error during headless generation: {e}")
    finally:
        headless_client.close()

if __name__ == '__main__':
    main()