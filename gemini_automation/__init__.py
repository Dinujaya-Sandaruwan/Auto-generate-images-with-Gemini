"""
Gemini Automation — Playwright-based image generation package.
"""

from .auth import login, logout, session_exists
from .generator.image_generator import generate_image

__version__ = "2.0.0"
__all__ = ["login", "logout", "session_exists", "generate_image"]
