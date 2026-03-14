---
name: research-quality-measurement
description: Rubric for verifying bug/codebase research artifacts. Use when reviewing research documents before implementing fixes.
license: MIT
---

## Purpose
Provide a consistent rubric to rate the quality of bug/codebase research artifacts (for example, `codebase-research.md`) before implementation.

## Quality Levels

### Level A — Audit‑Ready (PASS)
Research is precise enough to be used as an implementation source of truth.
- Every code claim includes **file path + exact line numbers**.
- Snippets **match the current repository** exactly.
- All referenced symbols/routes/commands are verified against source.
- Includes **repro steps** and a clear explanation of root cause.
- Notes assumptions, environment constraints, and edge cases.

### Level B — Implementation‑Ready with Minor Issues (PASS)
Research is usable but has small gaps.
- Most claims include file:line references; a few are missing line numbers.
- Snippets generally match, with minor formatting drift.
- Root cause likely correct; a few edge cases not discussed.

### Level C — Partially Reliable (FAIL)
Research contains material issues that can mislead implementation.
- Multiple missing/incorrect file:line references.
- Snippets are paraphrased or don’t match current source.
- Root cause is plausible but not proven with code evidence.

### Level D — Unreliable / Speculative (FAIL)
Research is not suitable for implementation.
- No verifiable references; relies on guesswork.
- Incorrect descriptions of routes/symbols/files.

## Required Output Fields (for verifiers)
When writing a verification report, include:
- Pass/Fail
- Level (A–D)
- Reasoning mapped to checks above
- Concrete discrepancies: claim → expected → actual
- References (file:line)
