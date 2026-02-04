---
name: context-summarizer
description: |
  Automatically generate conversation context summaries for seamless session continuity. Use when:
  - User says "summarize", "generate summary", or "save context"
  - Token usage exceeds 80% (auto-suggest)
  - Periodic summarization every N turns
  - Starting a new conversation (recover context from previous session)
  
  Output:
  - Mixed format (human-readable text + machine-readable JSON)
  - Saves to local file + OpenCode session
  - ~2000 words (2-minute read)
  
  Includes:
  - Project status (phase, progress, completion %)
  - Pending tasks (TODO list, priority)
  - Technical decisions (key decisions, alternatives, rationale)
  - Code context (current files, recent changes, architecture patterns)
  - Conversation history (key discussions, conclusions, pending items)
---

# Context Summarizer

## Quick Start

### Manual Trigger

Triggered when user says:
- "总结一下" / "summarize" / "generate summary"
- "保存上下文" / "save context"
- "会话总结" / "session summary"

### Auto Detection

System monitors token usage. When >80%:
```
⚠️ Context usage at 80%. Generate Context Summary for new session continuity?
[Y/n]
```

### Periodic Summarization

Automatic after every N turns (configurable, default: 10 turns)

## Output Format

### 1. Human-Readable Text

```markdown
# Context Summary

## Project Status
**Project Name** - Description
- Current Phase: Phase X
- Completion: XX/XX tasks (XX%)
- Pending: Task X, Task Y

## Pending Tasks
🔴 High Priority:
- Task X: Description

🟡 Medium Priority:
- Task Y: Description

## Technical Decisions
✅ Confirmed:
- Decision 1: Rationale
- Decision 2: Rationale

## Code Context
📁 Current Files:
- src/file1.py
- src/file2.py

📝 Recent Changes:
- Changed file3.py
- Added new feature

## Conversation History
💬 Key Discussions:
- Discussion 1
- Discussion 2

✅ Confirmed:
- Item 1
- Item 2

❓ Pending:
- Item 3
```

### 2. Machine-Readable JSON

```json
{
  "version": "1.0",
  "generated_at": "ISO8601-timestamp",
  "session_id": "session_abc123",
  "project": {
    "name": "Project Name",
    "description": "Brief description",
    "phase": 8,
    "total_tasks": 50,
    "completed_tasks": 47,
    "completion_rate": 0.94,
    "pending_tasks": [
      {
        "id": "38.7",
        "name": "Task Name",
        "priority": "high",
        "status": "pending"
      }
    ]
  },
  "tech_decisions": [
    {
      "decision": "Decision description",
      "status": "confirmed",
      "reason": "Why this decision"
    }
  ],
  "code_context": {
    "current_files": ["src/file1.py"],
    "recent_changes": ["Changed file2.py"],
    "architecture_patterns": ["pattern1", "pattern2"]
  },
  "conversation_history": {
    "key_discussions": ["Discussion 1"],
    "confirmed_items": ["Item 1"],
    "pending_confirmations": ["Item 2"]
  },
  "recovery_instructions": {
    "read_first": ["README.md", "AGENTS.md"],
    "continue_from": "Task 38.7",
    "key_context": "Brief context for new conversation"
  }
}
```

## Usage

### 1. Manual Summarization

When user triggers:

```python
summary = generate_summary(
    session_id="current_session",
    output_format="both",
    include_sections=["project", "tasks", "decisions", "code", "history"]
)
```

### 2. Auto Detection

```python
if get_token_usage() > 0.8:
    suggest_summary = True
```

### 3. Recovery in New Session

```python
# New session starts
summary_text = read_file("session_summary.md")
summary_json = read_file("session_summary.json")

# Inject into context
inject_into_context(summary_text)
```

## Save Locations

| Location | Format | Purpose |
|-----------|---------|---------|
| `./session_summary.md` | Text | Human reading |
| `./session_summary.json` | JSON | Machine processing |
| OpenCode Session | All | Session management |

## Recovery Workflow

### For New Sessions

1. **Read Summary** (2 minutes)
   - Read `session_summary.md`
   - Check `session_summary.json`

2. **Check TODO**
   - Read `AGENTS.md` for current TODO list
   - Identify highest priority pending task

3. **Continue Work**
   - Reference `code_context.current_files`
   - Start from `recovery_instructions.continue_from`

4. **Verify Understanding**
   - Confirm `conversation_history.pending_confirmations`
   - Ask user if unclear

## Integration

### OpenCode Session Integration

```python
# Save to session
session_save(summary_text, format="markdown")
session_save(summary_json, format="json")

# Read from session
summary = session_read(session_id="previous_session")
```

### Local File Integration

```python
# Save
save_to_file(summary_text, "session_summary.md")
save_to_file(summary_json, "session_summary.json")

# Read
summary_text = read_file("session_summary.md")
summary_json = read_file("session_summary.json")
```

## Configuration

### Auto-Trigger Thresholds

| Metric | Default | Configurable |
|--------|---------|-------------|
| Token usage warning | 80% | Yes |
| Periodic turns | 10 | Yes |
| Max summary length | 2000 words | Yes |

### Include Sections

Available sections:
- `project` - Project status
- `tasks` - Pending tasks
- `decisions` - Technical decisions
- `code` - Code context
- `history` - Conversation history

All included by default. Specify subset:
```python
include_sections=["project", "tasks"]
```

## Examples

### Example 1: User Request

**User**: "总结一下"

**AI**: Generates summary and shows:

```
# Context Summary

## Project Status
**Polymarket Insider Hunter** - AI intelligence monitoring system
- Current Phase: Phase 8 - AI Monitor System
- Completion: 47/50 tasks (94%)
- Pending: Task 38.7, 38.8, 38.9

## Pending Tasks
🔴 High Priority:
- Task 38.7: Polymarket Linker
- Task 38.9: System Integration

🟡 Medium Priority:
- Task 38.8: Integration Tests

## Technical Decisions
✅ Confirmed:
- Taiji Yin-Yang dual system architecture
- Pure API solution (no iframe)
- Event classification: P0-P1 prediction, P2-P3 information

## Code Context
📁 Current Files:
- src/collectors/arxiv.py
- src/collectors/github.py
- src/intelligence/ai_event_detector.py
- config/ai-sources.json

📝 Recent Changes:
- Completed Tasks 38.3-38.6 (collectors + detector)
- Added AI sources config

## Conversation History
💬 Key Discussions:
- Data classification: prediction vs information
- Polymarket association confirmation
- Task merge: 33→38.9

✅ Confirmed:
- cs.CL/CV added to arXiv monitoring
- GitHub repos (23 AI projects)
- Classification threshold: arXiv≥0.3, GitHub≥0.4

Saved to:
- session_summary.md
- session_summary.json

Ready for new session recovery! 🚀
```

### Example 2: Auto Detection

**System**: Token usage at 85%

**AI**: 
```
⚠️ Context usage at 85%. Generate Context Summary for new session continuity?
[Y/n]
```

### Example 3: New Session Recovery

**New Session Starts**:

**AI** (reads previous summary):
```
# Recovering from Previous Session

## Quick Status
**Polymarket Insider Hunter** - 94% complete
- Continue from: Task 38.7 Polymarket Linker
- Key context: AI monitor system development

## Immediate Actions
1. Read AGENTS.md for current TODO
2. Check src/collectors/ for current files
3. Start Task 38.7 Polymarket Linker

## Pending Confirmations
- Polymarket linker implementation details

Would you like me to continue from Task 38.7? [Y/n]
```

## Best Practices

### When to Generate

✅ DO:
- Token usage >80%
- After completing significant milestones
- Before complex refactoring
- When user asks

❌ DON'T:
- In the middle of simple tasks
- Every single turn
- Without user consent (unless auto-trigger)

### What to Include

✅ DO:
- Focus on actionable context
- Include specific file paths
- List clear pending items
- Highlight key decisions

❌ DON'T:
- Include every detail
- Add unnecessary context
- Duplicate README content
- Omit critical decisions

### Recovery Speed

**Target**: 2-minute read (~2000 words)

**Structure**:
- Status summary: 200 words
- Pending tasks: 500 words
- Technical decisions: 300 words
- Code context: 500 words
- History: 500 words

## Troubleshooting

### Summary Too Long

Reduce `max_words` or exclude sections:
```python
generate_summary(max_words=1500, exclude=["history"])
```

### Missing Context

Check `session_summary.json` for complete data:
```bash
cat session_summary.json | jq '.'
```

### Recovery Failed

1. Read `README.md`
2. Read `AGENTS.md`
3. Ask user for context
4. Regenerate summary if needed
