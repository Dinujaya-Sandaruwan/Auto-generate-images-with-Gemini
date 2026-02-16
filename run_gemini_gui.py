import os
from gemini_automation import GeminiClient

def main():
    print("--- Generating Image using GUI Browser ---")
    client = GeminiClient(headless=False, wait_timeout=120)