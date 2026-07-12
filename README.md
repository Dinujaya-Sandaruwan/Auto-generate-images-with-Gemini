# Auto-generate-images-Gemini

A Python automation toolkit for generating images using Google Gemini through browser automation. It handles authentication, session persistence, single image generation, and batch processing — all from the command line or via a Python API.

---

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Authentication](#authentication)
  - [Login](#login)
  - [Logout](#logout)
- [Generating Images](#generating-images)
  - [Quick Start](#quick-start)
  - [How to Set Your Prompt](#how-to-set-your-prompt)
  - [Headless Mode](#headless-mode)
  - [GUI Mode](#gui-mode)
- [Batch Processing](#batch-processing)
- [Python API](#python-api)
  - [Single Image](#single-image)
  - [Batch via API](#batch-via-api)
  - [GeminiClient Options](#geminiclient-options)
- [CLI Reference](#cli-reference)
- [Output](#output)
- [Troubleshooting](#troubleshooting)

---

## Requirements

- Python 3.8+
- Google Chrome installed
- A Google account with access to [Gemini](https://gemini.google.com)

---

## Installation

1. Clone or download the project.

2. Install Python dependencies:

```bash
pip install -r requirements.txt
```

3. Install Playwright browsers (required for session management):

```bash
playwright install chromium
```

Alternatively, install the package directly:

```bash
pip install .
```

---

## Authentication

This tool uses Playwright to open a real Chromium browser and saves your Google session locally so you only have to log in once.

### Login

Run the login command. A Chromium browser window will open and navigate to Gemini:

```bash
python run_gemini.py login
```

- Sign in to your Google account in the browser window that opens.
- Once you are signed in and see the Gemini chat interface, press **Ctrl+C** in the terminal to save your session and exit.

Your session is stored in a local `.gemini_session_profile` folder. You do not need to log in again unless the session expires or you explicitly log out.

> **Note:** The session is tied to your machine. Do not share the `.gemini_session_profile` folder with anyone.

---

### Logout

To clear your saved session and start fresh:

```bash
python run_gemini.py logout
```

This deletes the `.gemini_session_profile` folder. You will need to run `login` again before generating images.

---

## Generating Images

### Quick Start

Make sure you have logged in first, then run:

```bash
python run_gemini.py
```

This runs the generator using the default prompt defined in `run_gemini.py`.

---

### How to Set Your Prompt

Open `run_gemini.py` and find the configuration block near the top:

```python
# ---------------------------------------------------------------------------
# Configure your prompt here
# ---------------------------------------------------------------------------
PROMPT = (
    "A lone astronaut standing on a vibrant alien planet with two moons "
    "in the sky, bioluminescent flora surrounding them, cinematic lighting, "
    "ultra detailed, 8k"
)
TITLE = "alien_planet_astronaut"   # used as the output filename
OUTPUT_DIR = "generated_images"    # folder where the image will be saved
# ---------------------------------------------------------------------------
```

- **`PROMPT`** — The text description of the image you want to generate. Be as descriptive as possible for better results.
- **`TITLE`** — The filename (without extension) for the saved image. Use underscores instead of spaces.
- **`OUTPUT_DIR`** — The folder where generated images are saved. It will be created automatically if it does not exist.

After editing, save the file and run:

```bash
python run_gemini.py generate
```

Or just:

```bash
python run_gemini.py
```

---

### Headless Mode

Runs the browser invisibly in the background. No window pops up. Ideal for running on a server or automating quietly:

```bash
python run_gemini_headless.py
```

Or via the CLI flag:

```bash
gemini-automation "Your prompt here" --headless
```

---

### GUI Mode

Opens a visible browser window so you can watch the automation in real time. Useful for debugging:

```bash
python run_gemini_gui.py
```

To change the prompt in these scripts, open the respective file and edit the `prompt` variable in the `main()` function:

```python
prompt = "A majestic cyberpunk cityscape at sunset, neon lights reflecting on wet streets"
```

---

## Batch Processing

Batch mode lets you generate multiple images from a list of titles automatically. Each title is turned into a prompt and processed one by one. Successfully processed titles are removed from the list so the batch can be safely interrupted and resumed.

### 1. Create a `titles.json` file

```json
{
  "titles": [
    "How to Build a REST API in Python",
    "10 Tips for Better Sleep",
    "Introduction to Machine Learning",
    "Best Hiking Trails in Europe"
  ]
}
```

Each string in the `"titles"` array becomes the subject of a generated image. The tool automatically wraps it in a prompt like:

```
Make a blog thumbnail for How to Build a REST API in Python
```

### 2. Run batch mode

```bash
gemini-automation --batch --json-file titles.json
```

With a logo overlay:

```bash
gemini-automation --batch --json-file titles.json --logo logo.png
```

- Titles are processed one at a time.
- After each successful generation, the title is removed from `titles.json`.
- If a title fails, it is moved to the end of the list and retried after the others.
- You can safely stop and restart the batch at any time — it picks up from where it left off.

---

## Python API

You can use `GeminiClient` directly in your own Python scripts for full control.

### Single Image

```python
from gemini_automation import GeminiClient

client = GeminiClient(
    headless=True,          # True = no browser window
    output_dir="my_images"  # folder to save images
)

image_path = client.generate_image(
    prompt="A futuristic city floating in the clouds, golden hour lighting, ultra detailed",
    title="floating_city"   # output filename
)

print(f"Saved to: {image_path}")
client.close()
```

### With a Logo

Pass a path to a logo image and it will be uploaded alongside the prompt:

```python
image_path = client.generate_image(
    prompt="A blog thumbnail for Python tips",
    title="python_tips",
    logo_path="logo.png"
)
```

### Batch via API

```python
from gemini_automation import GeminiClient

client = GeminiClient(headless=True, output_dir="generated_images")

images = client.process_batch(
    json_file="titles.json",
    logo_path="logo.png"     # optional
)

print(f"Generated {len(images)} images")
client.close()
```

### GeminiClient Options

| Parameter | Type | Default | Description |
|---|---|---|---|
| `headless` | `bool` | `False` | Run browser without a visible window |
| `output_dir` | `str` | `"generated_images"` | Folder to save generated images |
| `session_dir` | `str` | `".gemini_session"` | Folder used to store session cookies |
| `wait_timeout` | `int` | `30` | Max seconds to wait for page elements |
| `remote_debug` | `bool` | `False` | Attach to an existing Chrome instance via remote debugging |

---

## CLI Reference

If installed via `pip install .`, you can use the `gemini-automation` command directly:

```bash
# Single image
gemini-automation "A dragon flying over a medieval castle"

# Single image with logo
gemini-automation "A dragon flying over a medieval castle" --logo logo.png

# Headless mode
gemini-automation "A dragon flying over a medieval castle" --headless

# Batch mode
gemini-automation --batch --json-file titles.json

# Custom output directory
gemini-automation "Your prompt" --output-dir my_folder

# Custom wait timeout (useful for slow connections)
gemini-automation "Your prompt" --wait-timeout 60

# Clear saved session
gemini-automation --clear-session
```

All available flags:

| Flag | Default | Description |
|---|---|---|
| `--batch` | off | Enable batch mode using a JSON file |
| `--json-file` | `titles.json` | Path to the batch titles JSON file |
| `--logo` | `logo.png` | Path to logo image to overlay |
| `--headless` | off | Run without a browser window |
| `--output-dir` | `generated_images` | Directory to save output images |
| `--wait-timeout` | `30` | Seconds to wait for elements to appear |
| `--clear-session` | off | Delete the saved session and exit |

---

## Output

All generated images are saved to the `generated_images` folder by default (or whichever directory you specify). Filenames are derived from the `title` parameter or the `TITLE` variable in `run_gemini.py`. If no title is given, a timestamp is used as the filename.

```
generated_images/
  alien_planet_astronaut.png
  floating_city.png
  How_to_Build_a_REST_API_in_Python.png
```

---

## Troubleshooting

**"No saved session found"**
Run `python run_gemini.py login` and complete the Google sign-in flow.

**"Could not find chat input. Session may have expired"**
Your session has expired. Run `python run_gemini.py logout` followed by `python run_gemini.py login` to re-authenticate.

**Image generation times out**
Gemini can be slow. Try increasing the timeout:
```python
client = GeminiClient(wait_timeout=120)
```
Or via the CLI:
```bash
gemini-automation "Your prompt" --wait-timeout 120
```

**Browser fails to launch**
Make sure Playwright browsers are installed:
```bash
playwright install chromium
```
