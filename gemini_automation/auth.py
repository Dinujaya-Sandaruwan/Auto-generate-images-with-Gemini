"""
Authentication management using Playwright persistent browser contexts.

Phase 1 — login():
  Opens a visible Chromium window. The user signs in to Google normally.
  Sign-in is confirmed by watching the URL change to gemini.google.com/app.
  The full session (cookies + storage) is persisted in SESSION_DIR so
  the headless generation phase can reuse it without logging in again.

Phase 2 — session is reused automatically by image_generator.py.
"""

import shutil
import time
from pathlib import Path
from playwright.sync_api import sync_playwright, TimeoutError as PWTimeout

SESSION_DIR = Path(".gemini_session_profile")
GEMINI_URL = "https://gemini.google.com"
SIGNED_IN_URL = "gemini.google.com/app"   # URL fragment that only appears after login


def login():
    """
    Open a visible browser, navigate to Gemini, and wait for the user to
    complete Google sign-in.  Detects success by watching for the URL to
    change to gemini.google.com/app (the main chat page).
    """
    SESSION_DIR.mkdir(parents=True, exist_ok=True)

    with sync_playwright() as pw:
        context = pw.chromium.launch_persistent_context(
            user_data_dir=str(SESSION_DIR),
            headless=False,
            slow_mo=100,
            args=[
                "--disable-blink-features=AutomationControlled",
                "--start-maximized",
            ],
            no_viewport=True,           # respect the maximized window size
            ignore_https_errors=True,
        )

        page = context.pages[0] if context.pages else context.new_page()
        page.goto(GEMINI_URL, wait_until="domcontentloaded", timeout=30_000)

        # Already signed in from a previous session?
        if SIGNED_IN_URL in page.url:
            print("Already signed in.")
            context.close()
            return

        print("=" * 60)
        print("Sign in to Google in the browser window that just opened.")
        print("The window will close automatically once you are signed in.")
        print("=" * 60)