"""
Gemini Image Generator — CLI entry point.

Usage:
    python run_gemini.py login      # Open browser, sign in to Google, save session
    python run_gemini.py logout     # Clear saved session
    python run_gemini.py generate   # Generate an image (headless, uses saved session)
    python run_gemini.py            # Same as generate
"""

import sys
import os
from gemini_automation.auth import login, logout, session_exists
from gemini_automation.generator.image_generator import generate_image

# ---------------------------------------------------------------------------
# Configure your prompt here
# ---------------------------------------------------------------------------
PROMPT = (
    "A lone astronaut standing on a vibrant alien planet with two moons "
    "in the sky, bioluminescent flora surrounding them, cinematic lighting, "
    "ultra detailed, 8k"
)
TITLE = "alien_planet_astronaut"
OUTPUT_DIR = "generated_images"
# ---------------------------------------------------------------------------


def cmd_login():
    login()


def cmd_logout():
    logout()


def cmd_generate():
    if not session_exists():
        print("No saved session found. Run login first:")
        print("  python run_gemini.py login")
        sys.exit(1)

    print("=" * 60)
    print("Generating image (headless)")
    print("=" * 60)
    print(f"Prompt: {PROMPT}\n")

    try:
        path = generate_image(prompt=PROMPT, title=TITLE, output_dir=OUTPUT_DIR)
        print(f"\nDone. Image saved to: {os.path.abspath(path)}")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    command = sys.argv[1] if len(sys.argv) > 1 else "generate"

    if command == "login":
        cmd_login()
    elif command == "logout":
        cmd_logout()
    elif command in ("generate", "gen"):
        cmd_generate()
    else:
        print(f"Unknown command: {command}")
        print("Usage: python run_gemini.py [login|logout|generate]")
        sys.exit(1)
