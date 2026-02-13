"""
Image generation using a headless Playwright browser context.
Reuses the persistent session saved by auth.login().
"""

import time
import base64
from pathlib import Path
from datetime import datetime
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

from ..auth import SESSION_DIR, GEMINI_URL, session_exists

OUTPUT_DIR = Path("generated_images")


def _sanitize(name: str) -> str:
    safe = "".join(c if (c.isalnum() or c in " _-") else "_" for c in name)
    return safe.strip()[:100]


def generate_image(prompt: str, title: str = None, output_dir: str = None) -> str:
    """
    Generate an image on Gemini using the saved session.
    Returns the absolute path to the saved image file.
    """
    if not session_exists():
        raise RuntimeError(
            "No saved session found. Run `python run_gemini.py login` first."
        )

    save_dir = Path(output_dir) if output_dir else OUTPUT_DIR
    save_dir.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        print("Starting headless browser...")
        context = pw.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--window-size=1920,1080",
            ],
            viewport={"width": 1920, "height": 1080},
            ignore_https_errors=True,
            accept_downloads=True,
        )

        page = context.pages[0] if context.pages else context.new_page()

        try:
            print(f"Navigating to {GEMINI_URL}...")
            page.goto(GEMINI_URL, wait_until="domcontentloaded", timeout=30_000)
            time.sleep(3)

            # Confirm signed in (URL should contain /app)
            if "gemini.google.com/app" not in page.url and "gemini.google.com" in page.url:
                # Try waiting a bit for redirect
                try:
                    page.wait_for_url("**/app**", timeout=10_000)
                except PWTimeout:
                    pass

            print(f"Current URL: {page.url}")

            # Find the chat input
            print("Looking for chat input...")
            input_sel = "div[contenteditable='true'], textarea"
            try:
                page.wait_for_selector(input_sel, state="visible", timeout=15_000)
            except PWTimeout: