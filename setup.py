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
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/gemini-automation",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Internet :: WWW/HTTP :: Browsers",
    ],
    python_requires=">=3.8",
    install_requires=[
        "selenium>=4.15.0",
        "requests>=2.31.0",
    ],
    entry_points={
        "console_scripts": [
            "gemini-automation=gemini_automation.cli:main",
        ],
    },
    keywords="gemini, automation, selenium, image-generation, ai, browser-automation",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/gemini-automation/issues",
        "Source": "https://github.com/yourusername/gemini-automation",
        "Documentation": "https://github.com/yourusername/gemini-automation#readme",
    },
)
