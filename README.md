# ds-bridge

A thin bridge that hands a written project roadmap to DeepSeek and lets it write the code straight to disk.

## How it works

1. You write a roadmap (a markdown file describing what to build).
2. `ds-bridge.py` sends it to DeepSeek (`deepseek-v4-flash`) with a system prompt instructing it to output complete files.
3. Each `FILE: <path> ... END_FILE` block in the response is parsed and written under the target project folder.
4. If DeepSeek hits something ambiguous, it can emit `QUESTION_FOR_CLAUDE: ...` to pause and ask before continuing — you answer in the terminal and it resumes.

## Setup

```bash
pip install openai
python3 setup_key.py   # stores your DeepSeek API key in config.py (gitignored)
```

## Usage

Install the `ds` wrapper on your PATH (e.g. `~/.local/bin/ds`):

```bash
#!/usr/bin/env bash
# ds <target_project_folder> <roadmap_file>
exec python3 /path/to/ds-bridge/ds-bridge.py "${2}" "${1}"
```

Then:

```bash
ds ~/projects/myapp/ roadmap.md
```
