"""Command-line interface for Gemini automation."""

import argparse
import sys
from pathlib import Path
from .client import GeminiClient


def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description="Automate Gemini website to generate images and download them",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate a single image
  gemini-automation "A beautiful sunset over mountains"

  # Generate with logo
  gemini-automation "A beautiful sunset" --logo logo.png

  # Batch process from JSON file
  gemini-automation --batch --json-file titles.json --logo logo.png

  # Run in headless mode
  gemini-automation "A cat" --headless

  # Clear session and start fresh
  gemini-automation --clear-session
        """
    )
    
    parser.add_argument(
        "prompt",
        type=str,
        nargs='?',
        help="Text prompt describing the image to generate (or use --batch for batch processing)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all titles from titles.json file"
    )