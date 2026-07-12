# Auto-generate-images-Gemini

A Python automation toolkit for generating images using Google Gemini through browser automation.

## Features
- **Browser Automation**: Uses Selenium to interact with Gemini.
- **Session Management**: Handles login states and sessions effectively.
- **Multiple Modes**: Run visibly (GUI) or in the background (Headless).
- **Batch Processing**: Supports batch generation through easy-to-use examples.

## Requirements
- Python 3.8+
- Google Chrome & ChromeDriver
- Dependencies inside `requirements.txt` (Selenium, Requests, etc.)

## Installation

1. Clone or navigate to the project directory.
2. Install the required dependencies:
```bash
pip install -r requirements.txt
```
*(Alternatively, you can install the package directly using `pip install .`)*

## Usage

This tool provides multiple entry points depending on how you want to interact with the automation.

### Headless Mode (Background)
Run the automation entirely in the background without any visible browser popups:
```bash
python run_gemini_headless.py
```

### GUI Mode (Visible)
If you want to watch the automation run in a visible browser window (helpful for debugging or first-time setup):
```bash
python run_gemini_gui.py
```

### Advanced / Main CLI
Use the main runner for additional configuration or arguments (if configured in `cli.py`):
```bash
python run_gemini.py --help
```

## Examples
The `examples/` directory contains sample scripts showing how to use the underlying API programmatically:
- `examples/simple_example.py`: A quickstart for running a basic automation task.
- `examples/batch_example.py`: Demonstrates how to run multiple iterations or batch image generation tasks.
