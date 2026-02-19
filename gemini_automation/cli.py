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
        else:
            print("No saved session found")
        return 0
    
    # Create client
    client = GeminiClient(
        headless=args.headless,
        output_dir=args.output_dir,
        wait_timeout=args.wait_timeout
    )
    
    try:
        if args.batch:
            # Batch processing mode
            print("Starting batch processing...")
            generated_images = client.process_batch(
                json_file=args.json_file,
                logo_path=args.logo
            )
            print(f"\n✓ Batch processing complete! Generated {len(generated_images)} images")
            return 0
        else:
            # Single image mode
            if not args.prompt:
                parser.error("Either provide a prompt or use --batch flag")
            
            client.initialize()
            logo_path = args.logo if Path(args.logo).exists() else None
            image_path = client.generate_image(args.prompt, logo_path=logo_path)
            print(f"\n✓ Success! Image generated and saved to: {image_path}")
            return 0
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
        return 1
    except Exception as e:
        print(f"\n✗ Error: {str(e)}")
        return 1
    finally:
        client.close()


if __name__ == "__main__":
    sys.exit(main())
