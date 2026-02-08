"""Simple example of using Gemini Automation."""

from gemini_automation import GeminiClient


def main():
    """Simple example: generate a single image."""
    # Initialize client
    client = GeminiClient(
        headless=False,  # Set to True to run without browser window