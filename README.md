# bridge

A thin bridge that hands a written project roadmap to an LLM and lets it write the code straight to disk.

## How it works

1. You write a roadmap (a markdown file describing what to build).
2. `bridge.py` sends it to your configured model with a system prompt instructing it to output complete files.
3. Each `FILE: <path> ... END_FILE` block in the response is parsed and written under the target project folder.
4. If the model hits something ambiguous, it can emit `QUESTION_FOR_CLAUDE: ...` to pause and ask before continuing — you answer in the terminal and it resumes.

## Supported providers

- **Any OpenAI-compatible API** — DeepSeek, OpenAI, Groq, OpenRouter, local Ollama, etc. (set `PROVIDER = "openai"` with the right `BASE_URL`/`MODEL`)
- **Anthropic's native API** (set `PROVIDER = "anthropic"`)

## Setup

```bash
pip install openai   # only needed for the openai-compatible path
python3 setup_key.py   # asks for provider, base URL, model, and API key; writes config.py (gitignored)
```

## Usage

Install the `ds` wrapper on your PATH (e.g. `~/.local/bin/ds`):

```bash
#!/usr/bin/env bash
# ds <target_project_folder> <roadmap_file>
exec python3 /path/to/bridge/bridge.py "${2}" "${1}"
```

Then:

```bash
ds ~/projects/myapp/ roadmap.md
```
