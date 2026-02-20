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
        
        try:
            print("Loading saved session...")
            # First navigate to the domain to set cookies
            self.driver.get("https://gemini.google.com")
            time.sleep(2)
            
            # Load cookies
            with open(self.cookies_file, 'rb') as f:
                cookies = pickle.load(f)
            
            # Add each cookie
            cookies_added = 0
            for cookie in cookies:
                try:
                    # Remove domain if it starts with . (Selenium requirement)
                    if 'domain' in cookie and cookie['domain'].startswith('.'):
                        cookie['domain'] = cookie['domain'][1:]
                    self.driver.add_cookie(cookie)
                    cookies_added += 1
                except Exception:
                    # Some cookies might be invalid, skip them
                    continue
            
            if cookies_added > 0:
                # Refresh to apply cookies
                self.driver.refresh()
                time.sleep(3)
                print(f"✓ Session loaded successfully ({cookies_added} cookies)")
                return True
            else:
                print("⚠ No valid cookies could be loaded")
                return False
        except Exception as e:
            print(f"⚠ Could not load session: {e}")
            return False
    
    def clear(self):
        """Clear saved session."""
        if self.cookies_file.exists():
            self.cookies_file.unlink()
            print("✓ Session cleared")
            return True
        return False
    
    def is_logged_in(self):
        """Check if user is already logged in."""
        try:
            # Look for indicators that user is logged in
            # Check for sign-in buttons (if they exist, we're not logged in)
            sign_in_indicators = [
                "//button[contains(text(), 'Sign in')]",
                "//a[contains(text(), 'Sign in')]",
                "//button[contains(text(), 'Get started')]",
            ]
            
            for selector in sign_in_indicators:
                try:
                    element = self.driver.find_element(By.XPATH, selector)
                    if element.is_displayed():
                        return False
                except NoSuchElementException:
                    continue
            
            # Check for logged-in indicators (input field, chat interface, etc.)
            logged_in_indicators = [
                (By.CSS_SELECTOR, "textarea[aria-label*='Enter a prompt']"),
                (By.CSS_SELECTOR, "textarea[placeholder*='Enter a prompt']"),
                (By.CSS_SELECTOR, "div[contenteditable='true']"),
                (By.CSS_SELECTOR, "[role='textbox']"),
            ]
            
            for by, selector in logged_in_indicators:
                try:
                    element = self.driver.find_element(by, selector)
                    if element.is_displayed():
                        print("✓ Already logged in")
                        return True
                except NoSuchElementException:
                    continue
            
            # If we can't find clear indicators, assume not logged in
            return False
        except Exception as e:
            print(f"⚠ Could not determine login status: {e}")
            return False
