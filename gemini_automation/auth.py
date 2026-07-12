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
import threading
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
        print("Once signed in, close the browser window to continue.")
        print("=" * 60)

        # Wait up to 3 minutes for the URL to become .../app
        deadline = time.time() + 180
        signed_in = False
        while time.time() < deadline:
            if SIGNED_IN_URL in page.url:
                signed_in = True
                break
            time.sleep(1)

        if not signed_in:
            print("\nTimed out waiting for sign-in. Please run login again.")
            context.close()
            return

        # Give the page a moment to fully settle and write storage
        time.sleep(3)
        print("\nSign-in detected. Session saved.")
        print("=" * 60)
        print("Press Ctrl+C to exit.")
        print("=" * 60)

        # Keep the script alive until the user presses Ctrl+C
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            pass

        try:
            context.close()
        except Exception:
            pass

        print("\nSession saved. Done.")
        import sys; sys.exit(0)


def logout():
    """Delete the saved session."""
    if SESSION_DIR.exists():
        shutil.rmtree(SESSION_DIR)
        print("Session cleared. Run `python run_gemini.py login` to sign in again.")
    else:
        print("No saved session found.")


def session_exists() -> bool:
    return SESSION_DIR.exists() and any(SESSION_DIR.iterdir())
