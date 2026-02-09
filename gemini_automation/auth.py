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