"""Human-in-the-loop pending submission state."""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from common import PENDING_DIR, ROOT

PLAN_APPROVED = "plan.approved"
PR_APPROVED = "pr.approved"
STATUSES = (
    "collecting",
    "await_plan_approval",
    "generating",
    "await_pr_approval",
    "publishing",
    "done",
    "cancelled",
)


def pending_dir(thread_id: str) -> Path:
    safe = thread_id.strip().replace("/", "-").replace("..", "")
    if not safe:
        raise ValueError("thread_id is required")
    return PENDING_DIR / safe


def ensure_pending(thread_id: str) -> Path:
    path = pending_dir(thread_id)
    path.mkdir(parents=True, exist_ok=True)
    return path


def write_intake(thread_id: str, data: dict[str, Any]) -> Path:
    folder = ensure_pending(thread_id)
    intake_path = folder / "intake.json"
    intake_path.write_text(json.dumps(data, indent=2) + "\n")
    return intake_path


def read_intake(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text())


def set_status(thread_id: str, status: str, extra: dict[str, Any] | None = None) -> None:
    if status not in STATUSES:
        raise ValueError(f"invalid status: {status}")
    folder = ensure_pending(thread_id)
    payload: dict[str, Any] = {
        "status": status,
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }
    if extra:
        payload.update(extra)
    (folder / "status.json").write_text(json.dumps(payload, indent=2) + "\n")


def read_status(thread_id: str) -> dict[str, Any]:
    path = pending_dir(thread_id) / "status.json"
    if not path.is_file():
        return {"status": "collecting"}
    return json.loads(path.read_text())


def write_plan(thread_id: str, plan_md: str) -> Path:
    folder = ensure_pending(thread_id)
    plan_path = folder / "plan.md"
    plan_path.write_text(plan_md)
    set_status(thread_id, "await_plan_approval")
    return plan_path


def approve_plan(thread_id: str) -> Path:
    folder = ensure_pending(thread_id)
    if not (folder / "intake.json").is_file():
        raise ValueError(f"no intake.json in {folder}")
    (folder / PLAN_APPROVED).write_text(datetime.now(timezone.utc).isoformat() + "\n")
    set_status(thread_id, "generating")
    return folder / PLAN_APPROVED


def approve_pr(thread_id: str) -> Path:
    folder = ensure_pending(thread_id)
    if not (folder / PLAN_APPROVED).is_file():
        raise ValueError("plan not approved yet")
    (folder / PR_APPROVED).write_text(datetime.now(timezone.utc).isoformat() + "\n")
    set_status(thread_id, "publishing")
    return folder / PR_APPROVED


def cancel(thread_id: str) -> None:
    folder = pending_dir(thread_id)
    if folder.is_dir():
        set_status(thread_id, "cancelled")
        for marker in (PLAN_APPROVED, PR_APPROVED):
            path = folder / marker
            if path.is_file():
                path.unlink()


def plan_is_approved(folder: Path) -> bool:
    return (folder / PLAN_APPROVED).is_file()


def pr_is_approved(folder: Path) -> bool:
    return (folder / PR_APPROVED).is_file()


def resolve_pending_from_intake(intake_path: Path) -> Path | None:
    intake_path = intake_path.resolve()
    pending_root = PENDING_DIR.resolve()
    try:
        intake_path.relative_to(pending_root)
        return intake_path.parent
    except ValueError:
        return None


def intake_for_thread(thread_id: str) -> Path:
    path = pending_dir(thread_id) / "intake.json"
    if not path.is_file():
        raise ValueError(f"intake not found for thread {thread_id}")
    return path
