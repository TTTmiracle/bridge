#!/usr/bin/env python3
import sys
import os
import re
from pathlib import Path
from openai import OpenAI

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import DEEPSEEK_API_KEY

SYSTEM_PROMPT = """You are a code generation engine. You will receive a detailed project roadmap. Implement it exactly as specified. Write complete files with full code, no placeholders. When you encounter logic that is genuinely ambiguous or algorithmically complex beyond the spec, output a block starting with QUESTION_FOR_CLAUDE: followed by your question, then pause and wait for the answer before continuing. Output each file using this format: FILE: <relative/path/to/file> followed by the complete file contents, then END_FILE"""

MODEL = "deepseek-v4-flash"

client = OpenAI(
    api_key=DEEPSEEK_API_KEY,
    base_url="https://api.deepseek.com",
)


def parse_and_write_files(response_text: str, target_dir: Path) -> list[str]:
    """Parse FILE:/END_FILE blocks and write them to disk. Returns list of written paths."""
    pattern = re.compile(
        r"^FILE:\s*(.+?)\s*\n(.*?)^END_FILE",
        re.MULTILINE | re.DOTALL,
    )
    written = []
    for match in pattern.finditer(response_text):
        rel_path = match.group(1).strip()
        contents = match.group(2)
        dest = (target_dir / rel_path).resolve()
        if not dest.is_relative_to(target_dir.resolve()):
            print(f"  [!] SKIPPED {rel_path} (points outside the target folder)")
            continue
        try:
            dest.parent.mkdir(parents=True, exist_ok=True)
            dest.write_text(contents)
            print(f"  [+] wrote {rel_path}")
            written.append(rel_path)
        except Exception as e:
            print(f"  [!] ERROR writing {rel_path}")
            print(f"      Full path: {dest}")
            print(f"      Error: {e}")
            raise
    return written


def extract_questions(response_text: str) -> list[str]:
    questions = re.findall(r"QUESTION_FOR_CLAUDE:\s*(.+?)(?=\n|$)", response_text)
    return questions


def ask_deepseek(messages: list[dict]) -> str:
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        max_tokens=8192,
    )
    return response.choices[0].message.content


def run(roadmap_path: str, target_path: str):
    roadmap = Path(roadmap_path).expanduser().resolve()
    target = Path(target_path).expanduser().resolve()

    if not roadmap.exists():
        print(f"Error: roadmap file not found: {roadmap}")
        sys.exit(1)

    target.mkdir(parents=True, exist_ok=True)
    roadmap_text = roadmap.read_text()

    print(f"Roadmap : {roadmap}")
    print(f"Target  : {target}")
    print(f"Model   : {MODEL}")
    print("-" * 60)

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": roadmap_text},
    ]

    while True:
        print("Sending request to DeepSeek…")
        reply = ask_deepseek(messages)
        messages.append({"role": "assistant", "content": reply})

        # Debug: show first 2000 chars of response
        print(f"\n[DEBUG] Response preview:\n{reply[:2000]}\n...")

        written = parse_and_write_files(reply, target)
        if written:
            print(f"\n{len(written)} file(s) written.")

        questions = extract_questions(reply)
        if not questions:
            break

        print("\n" + "=" * 60)
        print("  QUESTION FROM DEEPSEEK (needs your answer before continuing)")
        print("=" * 60)
        for q in questions:
            print(f"\n  {q}")
        print("\n" + "=" * 60)
        print("Type your answer below (press Enter twice when done):\n")

        lines = []
        while True:
            line = input()
            if line == "" and lines and lines[-1] == "":
                break
            lines.append(line)
        answer = "\n".join(lines).strip()

        messages.append({"role": "user", "content": answer})
        print("\nResuming generation…\n" + "-" * 60)

    print("\nDone.")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: ds-bridge.py <roadmap_file> <target_project_folder>")
        sys.exit(1)
    run(sys.argv[1], sys.argv[2])
