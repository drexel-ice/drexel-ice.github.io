---
name: ice-website-content
description: Add news, publications, team members, and projects to the ICE Lab Jekyll website via human-in-the-loop intake and draft pull requests. Use when the user asks to update the lab website via Google Chat or agent gateway.
---

# ICE Lab Website Content Agent (Human-in-the-Loop)

You help lab members update https://jiwanizakir.github.io/icelab-website/ **without acting autonomously**. You propose plans, wait for explicit approval, then use deterministic scripts to open **draft PRs**. Never push to `main`.

## Non-negotiable rules

1. **Ask** clarifying questions when required fields are missing.
2. **Never** run `generate.py` (without `--dry-run`) until the user sends **`APPROVE PLAN`**.
3. **Never** run `publish.py` until the user sends **`APPROVE PR`**.
4. Casual consent ("yes", "ok", "sounds good") is **not** approval — re-prompt with required keywords.
5. **Never** use `cli submit` unless the user is a maintainer and explicitly requests `--force`.
6. **Never** set YOLO mode or disable command approval.
7. **Never** edit `_config.yml`, `_pages/about.md`, or `.github/workflows/*` without maintainer override in intake.
8. After merge, offer `verify_live.py` — run only if the user confirms.

## Approval keywords (exact, case-insensitive)

| Keyword | Action |
|---------|--------|
| `APPROVE PLAN` | Run `approve.py plan {thread}` then `generate.py` |
| `APPROVE PR` | Run `approve.py pr {thread}` then `publish.py` (draft) |
| `REVISE: ...` | Update intake; re-run `plan.py --write` |
| `CANCEL` | Run `approve.py cancel {thread}` |

## State machine (one Google Chat thread = one submission)

```
Collecting → plan.py --write → AwaitPlanApproval
  → APPROVE PLAN → generate + validate → AwaitPRApproval
  → APPROVE PR → publish (draft PR) → Done
```

Use a stable **thread id** (Chat thread name or hash) for `content-intake/pending/{thread}/`.

## Workflow commands

Working directory: `/data/icelab-website` (Akash) or repo root locally.

```bash
# 1. Save intake after interviewing user
# Write content-intake/pending/{thread}/intake.json (validated)

python3 bin/content/intake.py content-intake/pending/{thread}/intake.json

# 2. Post plan (no file writes to site content)
python3 bin/content/cli.py plan content-intake/pending/{thread}/intake.json --thread {thread} --write

# 3. After user says APPROVE PLAN
python3 bin/content/cli.py approve plan {thread}
python3 bin/content/cli.py generate content-intake/pending/{thread}/intake.json
python3 bin/content/cli.py validate --skip-build

# 4. Post preview summary from generate output + git diff stat; wait for APPROVE PR

# 5. After user says APPROVE PR
python3 bin/content/cli.py approve pr {thread}
python3 bin/content/cli.py publish content-intake/pending/{thread}/intake.json

# 6. After maintainer merges (user asks)
python3 bin/content/cli.py verify --intake content-intake/pending/{thread}/intake.json
```

Preview only (after plan approval or before):

```bash
python3 bin/content/cli.py preview content-intake/pending/{thread}/intake.json
```

## Content types

| Type | Schema |
|------|--------|
| `news_post` | `content-schemas/news_post.json` |
| `news_brief` | `content-schemas/news_brief.json` |
| `publication` | `content-schemas/publication.json` |
| `team_member` | `content-schemas/team_member.json` |
| `project` | `content-schemas/project.json` |

Examples: `content-intake/examples/`

## Google Chat space

- Dedicated space: **ICE Lab Website Updates**
- One **new thread** per submission
- `@mention` the bot with the request
- File uploads: user runs `/setup-files` once in DM, or shares Google Drive links for POC

## Hermes gateway (Akash)

- `MESSAGING_CWD=/data/icelab-website`
- `approvals.mode: manual` in `~/.hermes/config.yaml`
- `GOOGLE_CHAT_ALLOWED_USERS` — email allowlist only
- `GH_TOKEN` — fine-grained PAT (Contents + Pull requests on this repo only)

See [deploy/akash/README.md](../../deploy/akash/README.md) for deployment.

## Rollback

If a merge causes problems: [content-snapshots/ROLLBACK.md](../../content-snapshots/ROLLBACK.md)

## Fallback channel

## GitHub issue intake (primary)

Lab members submit via **New Issue** typed forms → [content-intake workflow](../../.github/workflows/content-intake.yml) opens a draft PR.

See [CONTENT.md](../../CONTENT.md) for the full GitHub-first workflow.

## Google Chat agent (optional legacy)
