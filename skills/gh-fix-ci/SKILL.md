---
name: gh-fix-ci
description: Inspect GitHub PR checks with gh, pull failing GitHub Actions logs, summarize failure context, then create a fix plan and implement after user approval. Use when a user asks to debug or fix failing PR CI/CD checks on GitHub Actions and wants a plan + code changes; for external checks (e.g., Buildkite), only report the details URL and mark them out of scope.
---

# Gh Pr Checks Plan Fix

## Overview

Use gh to locate failing PR checks, fetch GitHub Actions logs for actionable failures, summarize the failure snippet, then propose a fix plan and implement after explicit approval.

Prereq: ensure `gh` is authenticated (`gh auth login`), then run `gh auth status` with escalated permissions.

## Inputs

- `repo`: path inside the repo (default `.`)
- `pr`: PR number or URL (optional; defaults to current branch PR)
- `gh` authentication for the repo host

## Workflow

1. Verify gh authentication (`gh auth status`)
2. Resolve the PR (`gh pr view --json number,url`)
3. Inspect failing checks with `gh pr checks --json name,state,bucket,link`
4. For each failing check, pull logs: `gh run view <run_id> --log`
5. Summarize failures for the user
6. Create a fix plan and request approval
7. Implement after approval
8. Recheck status after changes
