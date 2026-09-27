#!/usr/bin/env python3
"""Run this once to store your provider config in config.py."""
import os
import sys

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")

print("Provider type:")
print("  1) OpenAI-compatible (DeepSeek, OpenAI, Groq, OpenRouter, Ollama, etc.)")
print("  2) Anthropic (Claude native API)")
choice = input("> ").strip()
provider = "anthropic" if choice == "2" else "openai"

if provider == "openai":
    base_url = input("Base URL (e.g. https://api.deepseek.com): ").strip()
    model = input("Model (e.g. deepseek-v4-flash): ").strip()
else:
    base_url = input("Base URL [https://api.anthropic.com]: ").strip() or "https://api.anthropic.com"
    model = input("Model (e.g. claude-sonnet-5): ").strip()

key = input("API key: ").strip()

if not base_url or not model or not key:
    print("Missing a value, aborting.")
    sys.exit(1)

with open(config_path, "w") as f:
    f.write(f'PROVIDER = "{provider}"\n')
    f.write(f'BASE_URL = "{base_url}"\n')
    f.write(f'MODEL = "{model}"\n')
    f.write(f'API_KEY = "{key}"\n')

print(f"Config saved to {config_path}")
