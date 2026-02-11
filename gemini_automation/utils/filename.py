"""Filename sanitization utilities."""

import re


def sanitize_filename(title):
    """
    Sanitize title to create a slug-like filename.
    
    Args:
        title: The title string to sanitize
        
    Returns:
        A slug-like filename string (lowercase, hyphens instead of spaces)