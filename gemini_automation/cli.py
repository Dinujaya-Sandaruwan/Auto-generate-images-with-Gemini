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
    parser.add_argument(
        "--json-file",
        type=str,
        default="titles.json",
        help="JSON file with titles (default: titles.json)"
    )
    parser.add_argument(
        "--logo",
        type=str,
        default="logo.png",
        help="Path to logo image file (default: logo.png)"
    )
    parser.add_argument(
        "--headless",
        action="store_true",
        help="Run browser in headless mode (no GUI)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="generated_images",
        help="Directory to save generated images (default: generated_images)"
    )
    parser.add_argument(
        "--wait-timeout",
        type=int,
        default=30,
        help="Maximum time to wait for elements in seconds (default: 30)"
    )
    parser.add_argument(
        "--clear-session",
        action="store_true",
        help="Clear saved session and start fresh"
    )
    
    args = parser.parse_args()
    
    # Clear session if requested
    if args.clear_session:
        session_dir = Path(".gemini_session")
        cookies_file = session_dir / "cookies.pkl"
        if cookies_file.exists():
            cookies_file.unlink()
            print("✓ Session cleared")