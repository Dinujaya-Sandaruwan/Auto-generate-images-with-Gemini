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