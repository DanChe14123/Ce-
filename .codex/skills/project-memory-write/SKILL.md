---
name: project-memory-write
description: Use when the user wants to store, update, or delete a stable project fact in local Mem0-backed memory.
---

# Project Memory Write

## Overview

Use this skill to write stable, evidence-backed project facts into local Mem0-backed memory.

This is the preferred write path after:
- explicit user confirmation that a fact should be remembered
- an approved `[memory-candidate]` from `session-checkpoint`
- correction of an outdated or incorrect stable fact

## Workflow

1. Verify that `.codex/project-memory.json` exists in the current project.
2. Confirm that the fact passes all four checks:
   - it is a stable fact, not a task-process item
   - it is likely to be reused across future threads
   - it is evidence-backed or explicitly confirmed by the user
   - it can be expressed as one short durable fact
3. Choose one operation:
   - `project-memory add --approve-stable --text "..."`
   - `project-memory update --approve-stable --id "..." --text "..."`
   - `project-memory delete --id "..."`
4. Keep each memory item concise and durable.
5. Prefer these categories only:
   - long-lived project rules
   - validated project decisions
   - evidence-backed stable facts
   - durable rejected constraints
   - confirmed project-relevant user preferences
6. Never store:
   - current progress
   - next actions
   - blockers
   - unresolved hypotheses
   - temporary TODOs or drafts
   - broad session summaries
   - secrets or credentials

## Required Output

Use these sections in order:

### Operation

- add, update, or delete

### Stable Fact

- The exact fact being written or corrected

### Result

- The memory id or deletion result

## Quality Bar

- One memory item should normally capture one stable fact.
- Prefer precise statements over narrative summaries.
- If the fact is not yet validated, stop and say so instead of writing it.
