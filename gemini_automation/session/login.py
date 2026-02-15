"""Login handling for Gemini."""

import time
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from .manager import SessionManager


class LoginHandler:
    """Handles login flow for Gemini."""
    
    def __init__(self, driver, session_manager):
        """
        Initialize login handler.
        
        Args:
            driver: Selenium WebDriver instance
            session_manager: SessionManager instance
        """
        self.driver = driver
        self.session_manager = session_manager
    
    def handle_login_if_needed(self, wait_time=60):
        """Handle Google login if required."""
        # Check if already logged in
        if self.session_manager.is_logged_in():