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

            if not logged_in:
                raise Exception(
                    "Login timed out — the Gemini chat input never appeared. "
                    "Please sign in faster or increase LOGIN_WAIT_SECONDS."
                )

            print("✓ Login detected!")
            # Persist cookies so the headless phase can reuse them
            self.session_manager.save()
            print("✓ Session cookies saved for headless phase.")
        else:
            # --- HEADLESS / STANDALONE PHASE ---
            # Load cookies saved during the login phase before navigating so
            # Google sees an authenticated session immediately.
            self.browser.navigate_to("https://gemini.google.com",
                                     wait_timeout=self.wait_timeout)
            time.sleep(2)
            self.session_manager.load()
            time.sleep(3)  # let the page re-render with the injected cookies

            if not self.login_handler.handle_login_if_needed(
                    wait_time=self.wait_timeout):
                raise Exception("Login failed. Run the login phase first.")

        self._initialized = True
    
    def generate_image(self, prompt, title=None, logo_path=None):
        """
        Generate a single image.
        
        Args:
            prompt: Text prompt describing the image to generate
            title: Title to use as filename (optional)
            logo_path: Optional path to logo image file to upload
        
        Returns:
            Path to the saved image file
        """
        if not self._initialized:
            self.initialize()
        
        # Clear chat
        self.generator.clear_chat()
        
        # Paste logo if provided
        if logo_path:
            logo_path_obj = Path(logo_path)
            if logo_path_obj.exists():
                self.generator.paste_image(logo_path)
                time.sleep(0.5)
        
        # Enter prompt
        if not self.generator.enter_prompt(prompt):
            raise Exception("Failed to enter prompt")
        
        # Submit prompt
        if not self.generator.submit_prompt():
            raise Exception("Failed to submit prompt")
        
        # Wait for image and download
        img_element = self.generator.wait_for_image_generation()
        image_path = self.generator.download_image(img_element, title=title)

        time.sleep(3)

        return image_path
    
    def process_batch(self, json_file="titles.json", logo_path="logo.png"):
        """
        Process all titles from JSON file, generating images for each.
        
        Args:
            json_file: Path to JSON file with titles
            logo_path: Path to logo image file
        
        Returns:
            List of generated image paths
        """
        import json
        
        json_path = Path(json_file)
        if not json_path.exists():
            raise FileNotFoundError(f"JSON file not found: {json_file}")
        
        logo_path_obj = Path(logo_path)
        if not logo_path_obj.exists():
            print(f"⚠ Warning: Logo file not found: {logo_path}")
            logo_path = None
        
        # Read titles from JSON
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        