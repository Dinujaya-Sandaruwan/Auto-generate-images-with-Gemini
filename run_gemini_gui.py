import os
from gemini_automation import GeminiClient

def main():
    print("--- Generating Image using GUI Browser ---")
    client = GeminiClient(headless=False, wait_timeout=120)
    try:
        client.initialize()
        prompt = "A majestic cyberpunk cityscape at sunset, neon lights reflecting on wet streets, high quality, highly detailed 8k"
        print(f"Generating image with prompt: '{prompt}'...")
        image_path = client.generate_image(prompt=prompt, title="cyberpunk_city_gui")
        print(f"Success! Image saved to: {os.path.abspath(image_path)}")