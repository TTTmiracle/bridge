#!/usr/bin/env python3
"""Run this once to store your DeepSeek API key in config.py."""
import os
import sys

config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "config.py")

key = input("Enter your DeepSeek API key: ").strip()
if not key:
    print("No key entered, aborting.")
    sys.exit(1)

with open(config_path, "w") as f:
    f.write(f'DEEPSEEK_API_KEY = "{key}"\n')

print(f"Key saved to {config_path}")
