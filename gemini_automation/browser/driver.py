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

        cmd = [
            chrome_bin,
            f"--remote-debugging-port={debug_port}",
            f"--user-data-dir={debug_profile}",
            "--no-first-run",
            "--no-default-browser-check",
        ]
        print(f"Launching Chrome with remote-debugging on port {debug_port}...")
        subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        # Poll until Chrome is listening (up to 20 s)
        deadline = time.time() + 20
        while time.time() < deadline:
            time.sleep(0.75)
            try:
                with socket.create_connection(("localhost", debug_port), timeout=1):
                    break
            except OSError:
                continue
        else:
            raise RuntimeError(
                f"Chrome did not open a debug port on {debug_port} within 20 seconds.\n"
                f"Chrome binary: {chrome_bin}"
            )
        time.sleep(1)  # small extra buffer

    # ------------------------------------------------------------------
    # Instance methods
    # ------------------------------------------------------------------

    def setup(self):
        """Setup and configure the Selenium WebDriver."""
        chrome_options = Options()

        if self.remote_debug:
            # Attach to an already-running Chrome instance
            chrome_options.add_experimental_option(
                "debuggerAddress", "localhost:9222"
            )
        else:
            if self.headless:
                chrome_options.add_argument("--headless=new")
                chrome_options.add_argument("--window-size=1920,1080")

            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option("useAutomationExtension", False)
            chrome_options.add_argument(
                "--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
            )

            # Isolated profile for the headless phase
            profile_dir = Path.cwd() / ".chrome_profile"
            profile_dir.mkdir(parents=True, exist_ok=True)
            chrome_options.add_argument(f"--user-data-dir={profile_dir.absolute()}")

            prefs = {
                "download.default_directory": str(self.output_dir.absolute()),