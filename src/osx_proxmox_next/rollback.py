from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import subprocess


@dataclass
class RollbackSnapshot:
    vmid: int
    path: Path


def create_snapshot(vmid: int) -> RollbackSnapshot:
    out_dir = Path.cwd() / "generated" / "snapshots"
    out_dir.mkdir(parents=True, exist_ok=True)
    ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    path = out_dir / f"vm-{vmid}-{ts}.conf"

    result = subprocess.run(
        ["qm", "config", str(vmid)],
        capture_output=True,
        text=True,
        check=False,
    )
    content = result.stdout if result.returncode == 0 else "# No existing VM config captured\n"
    path.write_text(content, encoding="utf-8")
    return RollbackSnapshot(vmid=vmid, path=path)


def rollback_hints(snapshot: RollbackSnapshot) -> list[str]:
    return [
        f"Review snapshot: {snapshot.path}",
        f"If needed: qm destroy {snapshot.vmid} --purge",
        "Re-apply previous known-good config from snapshot content.",
    ]
