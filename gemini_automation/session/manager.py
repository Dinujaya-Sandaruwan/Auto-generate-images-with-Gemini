"""Session cookie management."""

import pickle
import time
from pathlib import Path
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By


class SessionManager:
    """Manages session cookies for persistent login."""
    
    def __init__(self, driver, session_dir=".gemini_session"):
        """
        Initialize session manager.
        
        Args:
            driver: Selenium WebDriver instance
            session_dir: Directory to save session cookies
        """
        self.driver = driver
        self.session_dir = Path(session_dir)
        self.session_dir.mkdir(parents=True, exist_ok=True)
        self.cookies_file = self.session_dir / "cookies.pkl"
    
    def save(self):
        """Save current cookies to maintain session."""
        try:
            cookies = self.driver.get_cookies()
            with open(self.cookies_file, 'wb') as f:
                pickle.dump(cookies, f)
            print("✓ Session saved successfully")
            return True
        except Exception as e:
            print(f"⚠ Could not save session: {e}")
            return False
    
    def load(self):
        """Load saved cookies to maintain session."""
        if not self.cookies_file.exists():
            return False
        