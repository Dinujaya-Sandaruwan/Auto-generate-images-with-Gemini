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
                page.screenshot(path=str(save_dir / "debug_no_input.png"))
                raise RuntimeError("Could not find chat input. Session may have expired — run login again.")

            chat_input = page.locator(input_sel).first
            chat_input.click()
            time.sleep(0.5)
            chat_input.fill(prompt)
            time.sleep(0.5)
            print(f"Prompt entered: {prompt[:60]}...")

            # Take a screenshot to confirm the state before submitting
            page.screenshot(path=str(save_dir / "debug_before_submit.png"))

            # Click the send button — it's the only enabled button inside the input form
            # Try multiple selectors for the blue send/submit button
            submitted = False
            send_selectors = [
                # Most specific: enabled button with upward arrow aria-label
                "button[aria-label='Send message']",
                "button[aria-label='Submit']",
                "button[aria-label*='Send']",
                "button[aria-label*='send']",
                # Gemini's send button is inside the input container
                ".input-area button[type='submit']",
                # Last resort: any visible enabled button near the input
                "button.send-button",
                "button[data-testid='send-button']",
            ]

            for sel in send_selectors:
                try:
                    btn = page.locator(sel).first
                    if btn.is_visible(timeout=2_000) and btn.is_enabled():
                        btn.click()
                        submitted = True
                        print(f"Prompt submitted via: {sel}")
                        break
                except Exception:
                    continue

            if not submitted:
                # Fallback: press Enter in the input
                chat_input.press("Enter")
                submitted = True
                print("Prompt submitted via Enter key.")

            time.sleep(2)
            page.screenshot(path=str(save_dir / "debug_after_submit.png"))
            print("Waiting for image generation (up to 3 minutes)...")

            img_path = _wait_and_save(page, save_dir, title)
            return img_path

        finally:
            context.close()


def _wait_and_save(page, save_dir: Path, title: str = None, timeout: int = 180) -> str:
    """
    Wait for Gemini to finish generating the image, click the download button,
    and capture the downloaded file.
    """
    stem = _sanitize(title) if title else f"gemini_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    deadline = time.time() + timeout

    print("Waiting for image to finish generating...")

    # Step 1: wait until the "Creating your image" placeholder is gone
    # and a real img with a download button appears
    download_btn_sel = "button[aria-label='Download image'], button[aria-label*='ownload']"

    while time.time() < deadline: