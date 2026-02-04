# Context Summarizer Skill

Automatically generate conversation context summaries for seamless session continuity.

## Installation

```bash
npx skills add panglihaoshuai/context-summarizer-skill
```

## Usage

### Manual Trigger

Say "summarize", "generate summary", or "save context"

### Auto Detection

System monitors token usage and suggests summary when >80%

## Features

- Mixed output (human-readable + machine-readable)
- Saves to local file for session recovery
- ~2000 words summary
- Includes: project status, pending tasks, technical decisions, code context

## For Developers

Edit `scripts/generate_summary.py` to customize behavior.

## License

MIT
