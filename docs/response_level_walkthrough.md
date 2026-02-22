# Walkthrough — Verbosity Tightening & Markdown Transcript

## Changes Made

### 1. Tighter `ResponseLevel` prompts (`config.py`)

| Level | Behaviour |
|---|---|
| **Simple** | ## headings only + ONE short paragraph per section. **No bullets, no lists.** |
| **Intermediate** | ## headings + up to 4 bullets per section, one sentence each |
| **Advanced** | ## / ### headings, multi-bullet with rationale & trade-offs |
| **Expert** | Exhaustive depth, nested sections, no length limit |

Also added `MARKDOWN_FORMAT_INSTRUCTION` — a shared rule that forces both agents to always use `##` headings and emojis regardless of level.

### 2. `MARKDOWN_FORMAT_INSTRUCTION` injected into agents (`debate_agents.py`)
Both `ConsultantAgent` and `AdversarialArchitectAgent` now have the markdown rule baked into their system prompt **before** the level instruction, ensuring clean formatted output every time.

### 3. Live Markdown Transcript (`orchestrator.py`)
Every debate run now writes a transcript to:
```
debate_transcripts/debate_<YYYYMMDD_HHMMSS>_<level>.md
```
- File is written **incrementally** after each agent turn (safe if run is interrupted)
- Each turn rendered as a formatted block with emoji banner, turn number, and agent label
- A summary footer table is appended on completion

**Sample transcript structure:**
```markdown
# 🧠 Group Debate Transcript
> Generated: 2026-02-22 12:05:00
> Response Level: `SIMPLE`

## 📋 Debate Topic
...

## 🤝 Turn 1 — Lead Technical Consultant
[agent response in markdown]

## 🏗️ Turn 2 — Adversarial System Architect
[agent response in markdown]

## ✅ Debate Concluded
| Field | Value |
|---|---|
| Total turns | 4 |
| Concluded by | Adversarial_Architect approved the plan |
```
