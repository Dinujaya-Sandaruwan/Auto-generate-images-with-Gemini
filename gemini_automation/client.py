"""High-level client API for Gemini automation."""

import time
from pathlib import Path
from .browser import BrowserDriver
from .session import SessionManager, LoginHandler
from .generator import ImageGenerator


class GeminiClient:
    """High-level client for Gemini automation."""

    def __init__(self, headless=False, output_dir="generated_images",
                 session_dir=".gemini_session", wait_timeout=30,
                 remote_debug=False):
        """
        Initialize Gemini client.

        Args:
            headless:     Run browser in headless mode
            output_dir:   Directory to save generated images
            session_dir:  Directory to save/load session cookies
            wait_timeout: Maximum time to wait for elements (seconds)
            remote_debug: Attach to real Chrome via remote-debugging port.
                          Use this for the login phase so Selenium operates
                          inside the user's own browser profile.
        """
        self.browser = BrowserDriver(headless=headless, output_dir=output_dir,
                                     remote_debug=remote_debug)
        self.remote_debug = remote_debug
        self.session_dir = session_dir
        self.session_manager = None
        self.login_handler = None
        self.generator = None
        self.wait_timeout = wait_timeout
        self._initialized = False

    def initialize(self):
        """Initialize browser and handle login / session loading."""
        if self._initialized:
            return

        driver = self.browser.get_driver()

        session_dir_path = (Path(self.session_dir)
                            if isinstance(self.session_dir, str)
                            else self.session_dir)
        self.session_manager = SessionManager(driver, session_dir=session_dir_path)
        self.login_handler = LoginHandler(driver, self.session_manager)
        self.generator = ImageGenerator(driver, output_dir=str(self.browser.output_dir),
                                        wait_timeout=self.wait_timeout)

        if self.remote_debug:
            # --- LOGIN PHASE ---
            # Navigate to Gemini in the user's real Chrome window, then poll
            # until the chat textarea appears (meaning the user is logged in).
            self.browser.navigate_to("https://gemini.google.com",
                                     wait_timeout=self.wait_timeout)
            time.sleep(2)

            print("\n>>> Chrome is open at gemini.google.com")
            print(">>> Please sign in to your Google account in the browser.")
            print(f">>> Waiting up to {self.wait_timeout} seconds for login...")

            # Poll for the chat input field — its presence means login is done
            from selenium.webdriver.support.ui import WebDriverWait
            from selenium.webdriver.support import expected_conditions as EC
            from selenium.webdriver.common.by import By
            from selenium.common.exceptions import TimeoutException

            driver = self.browser.get_driver()
            logged_in_selectors = [
                "//textarea[contains(@aria-label,'Enter a prompt')]",
                "//textarea[contains(@placeholder,'Enter a prompt')]",
                "//*[@role='textbox']",
                "//div[@contenteditable='true']",
            ]

            deadline = time.time() + self.wait_timeout
            logged_in = False
            while time.time() < deadline:
                for sel in logged_in_selectors:
                    try:
                        el = driver.find_element("xpath", sel)
                        if el.is_displayed():
                            logged_in = True
                            break
                    except Exception:
                        pass
                if logged_in:
                    break
                time.sleep(2)
