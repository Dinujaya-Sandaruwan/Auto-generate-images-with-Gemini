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
            return True
        
        # Check if login is required (look for sign-in button or login prompt)
        sign_in_selectors = [
            "//button[contains(text(), 'Sign in')]",
            "//a[contains(text(), 'Sign in')]",
            "//button[contains(text(), 'Get started')]",
            "//button[contains(text(), 'Sign in to connect')]",
            "[data-testid='sign-in']",
            "//span[contains(text(), 'Sign in to connect')]",
        ]
        
        login_required = False
        for selector in sign_in_selectors:
            try:
                if selector.startswith("//"):
                    element = self.driver.find_element(By.XPATH, selector)
                else:
                    element = self.driver.find_element(By.CSS_SELECTOR, selector)
                
                if element.is_displayed():
                    login_required = True
                    break
            except NoSuchElementException:
                continue
        