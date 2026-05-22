---
name: research-repro-start
description: Use when the user asks to reproduce a paper, baseline, model, experiment, or reported result. This skill enforces the reproduction gate by requiring a matching repro-* OpenSpec change before analysis or implementation continues.
---

# Research Repro Start

## Overview

Use this skill as the mandatory entry point for reproduction work inside a research project.

This is a gate, not a suggestion. Do not continue into detailed analysis, coding, or execution until the reproduction state is properly established.

## Workflow

1. Verify the project has both a root `AGENTS.md` and an `openspec/` directory.
2. If either is missing, stop and tell the user to bootstrap the project first:
   - `retrofit-research-project <target_path>` for an existing project
   - `new-research-project <target_path>` for a new project
3. Read the project `AGENTS.md` before doing anything else.
4. If `.codex/project-memory.json` exists:
   - run `project-memory search --query "<paper title, first author, or task topic>"`
   - note any relevant stable facts before checking `OpenSpec`
5. Inspect active changes with `openspec list --json`.
6. Derive a change name using:
   - `repro-<firstauthor>-<year>-<topic>`
7. If there is exactly one matching active `repro-*` change:
   - read `proposal.md`
   - read `design.md`
   - read `tasks.md`
   - read `session-log.md` if it exists
   - summarize the current state before continuing
8. If there are multiple plausible matching changes:
   - stop and ask the user which one to resume
9. If there is no matching change:
   - use the `openspec-propose` workflow, not just `openspec new change`
   - create the full change so that `proposal.md`, `design.md`, and `tasks.md` exist
   - if `session-log.md` is missing after that, create it from `openspec/templates/session-log-template.md`
10. Only after the change is ready, continue into reproduction analysis or implementation.

## Required Output

Use these sections in order:

### Change Name

- The active or newly created `repro-*` change.

### Status

- Whether the change was restored or newly created.
- Which artifacts are present.

### Ready Context

- The reproduction target.
- The current stage of work.
- The key blocker, if any.

### First Next Action

- One concrete next step only.

## Quality Bar

- Do not treat a paper title alone as enough context if author/year/topic are ambiguous.
- Do not improvise task state in chat if `OpenSpec` should own it.
- Do not start code work before the reproduction change exists and has been read.
