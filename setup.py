"""Setup script for Gemini Automation package."""

from setuptools import setup, find_packages
from pathlib import Path

# Read README for long description
readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text() if readme_file.exists() else ""

setup(
    name="gemini-automation",
    version="1.0.0",
    description="A modular Python package for automating Google Gemini image generation",
    long_description=long_description,
    long_description_content_type="text/markdown",