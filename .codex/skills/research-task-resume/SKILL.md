---
name: research-task-resume
description: Use when the user wants to continue a paused long-running task, recover context in a new thread, or reopen project work after an interruption. This skill restores task state from project AGENTS and OpenSpec before new work begins.
---

# Research Task Resume

## Overview

Use this skill before continuing a long-running task in a fresh thread.

The goal is to restore project and task state before new reasoning starts.

## Workflow

1. Read the project root `AGENTS.md`.
2. If `.codex/project-memory.json` exists:
   - run `project-memory list --top-k 10`
   - if the user names a task, topic, or paper, also run `project-memory search --query "<named target>"`
   - note relevant stable facts before reading `OpenSpec`
3. Verify that `openspec/` exists.
4. Inspect active changes with `openspec list --json`.
5. If there are no active changes:
   - say so clearly
   - suggest whether the user likely needs a new `study-*`, `write-*`, or `repro-*` change
6. If there is exactly one active change, or the user names one explicitly:
   - read `proposal.md`
   - read `design.md`
   - read `tasks.md`
   - read `session-log.md` if it exists
7. If there are multiple active changes and the user did not specify one:
   - list the candidates briefly
   - ask which one to resume before doing new work
8. Summarize the restored state before continuing.

## Required Output

Use these sections in order:

### Active Change

- The change being resumed, or `none`.

### Objective

- The goal of the active task.

### Current State

- What is already done.

### Current Blockers

- The active blockers, if any.

### First Next Action

- One concrete first action for this session.

## Quality Bar

- Do not continue with fresh analysis until this recovery summary is complete.
- If `session-log.md` is missing, call that out explicitly instead of pretending the state is complete.
- Prefer reading the actual artifacts over relying on conversation memory.
