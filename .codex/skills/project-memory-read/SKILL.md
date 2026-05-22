---
name: project-memory-read
description: Use when the current project exposes Mem0-backed project memory and the task should recover stable facts before new reasoning begins.
---

# Project Memory Read

## Overview

Use this skill to recover stable project facts from local Mem0-backed memory before new reasoning starts.

This is the preferred memory entry point for:
- new long-running tasks
- resumed work in a fresh thread
- high-risk design, planning, or writing work

## Workflow

1. Verify that `.codex/project-memory.json` exists in the current project.
2. Run `project-memory status` to confirm the project memory namespace.
3. If the user named a paper, topic, task, or project target:
   - run `project-memory search --query "<target>"`
4. Otherwise:
   - run `project-memory list --top-k 10`
5. Only keep facts that are clearly relevant to the current request.
6. If no relevant facts exist, say so directly instead of inventing continuity.

## Required Output

Use these sections in order:

### Project Memory Status

- Whether project memory is connected.
- The active project memory id.

### Relevant Stable Facts

- The relevant evidence-backed facts recovered from Mem0.

### Gaps Or Conflicts

- Missing stable facts.
- Any apparent conflicts that need confirmation.

### First Next Action

- One concrete next action only.

## Quality Bar

- Do not treat Mem0 results as a replacement for `OpenSpec`.
- Do not retrieve broad chat summaries when a targeted search is possible.
- Do not present stale or weakly related memory items as current truth without qualification.
