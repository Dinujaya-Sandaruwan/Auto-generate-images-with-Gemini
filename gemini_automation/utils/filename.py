"""Filename sanitization utilities."""

import re


def sanitize_filename(title):
    """
    Sanitize title to create a slug-like filename.
    
    Args:
        title: The title string to sanitize
        
    Returns:
        A slug-like filename string (lowercase, hyphens instead of spaces)
    """
    if not title:
        return ""
    
    # Convert to lowercase
    safe_title = title.lower()
    
    # Replace spaces and underscores with hyphens
    safe_title = re.sub(r'[\s_]+', '-', safe_title)
    
    # Remove all characters except alphanumeric and hyphens
    safe_title = re.sub(r'[^a-z0-9\-]', '', safe_title)
    
    # Remove multiple consecutive hyphens
    safe_title = re.sub(r'-+', '-', safe_title)
    
    # Remove leading/trailing hyphens
    safe_title = safe_title.strip('-')
    
    # Limit length to avoid filesystem issues (max 255 chars for most filesystems)
    # Leave room for extension
    if len(safe_title) > 200:
        safe_title = safe_title[:200]
    
    # If empty after sanitization, use a default
    if not safe_title:
        safe_title = "untitled"
    
    return safe_title
