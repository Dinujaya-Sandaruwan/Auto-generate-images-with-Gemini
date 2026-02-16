"""Browser driver setup and management."""

import subprocess
import time
import socket
import shutil
from pathlib import Path

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException


class BrowserDriver:
    """Manages Selenium WebDriver setup and configuration."""

    def __init__(self, headless=False, output_dir="generated_images", remote_debug=False):
        """
        Args:
            headless:     Run in headless mode (generation phase).
            output_dir:   Directory to save generated images.
            remote_debug: Attach to a Chrome instance already running with
                          --remote-debugging-port=9222.  When True, headless
                          is ignored and no new Chrome process is spawned.
        """
        self.headless = headless
        self.remote_debug = remote_debug
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.driver = None

    # ------------------------------------------------------------------
    # Static helper — call this before creating a BrowserDriver instance
    # ------------------------------------------------------------------

    @staticmethod
    def launch_real_chrome(debug_port: int = 9222):
        """
        Launch a fresh Chrome window with a remote-debugging port so Selenium
        can attach to it.  A temporary profile is used to avoid clashing with
        any running Chrome instance.
        """
        chrome_bin = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        debug_profile = Path("/tmp/chrome-debug-profile")

        if not Path(chrome_bin).exists():
            raise FileNotFoundError(
                f"Chrome not found at:\n  {chrome_bin}\n"
                "Install Google Chrome or update the path in driver.py."
            )

        # Fresh temp profile each run — no lock conflicts
        if debug_profile.exists():
            shutil.rmtree(debug_profile, ignore_errors=True)
        debug_profile.mkdir(parents=True, exist_ok=True)
