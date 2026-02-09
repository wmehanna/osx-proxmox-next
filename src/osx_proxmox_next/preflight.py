from __future__ import annotations

from dataclasses import dataclass
import os
from pathlib import Path
import shutil


@dataclass
class PreflightCheck:
    name: str
    ok: bool
    details: str


def _find_binary(cmd: str) -> str | None:
    binary = shutil.which(cmd)
    if binary:
        return binary

    for prefix in ("/usr/sbin", "/sbin", "/usr/bin", "/bin"):
        candidate = Path(prefix) / cmd
        if candidate.exists():
            return str(candidate)
    return None


def _is_root() -> bool:
    try:
        return os.geteuid() == 0
    except AttributeError:
        return False


def run_preflight() -> list[PreflightCheck]:
    checks: list[PreflightCheck] = []
    for cmd in ("qm", "pvesm", "pvesh", "qemu-img"):
        binary = _find_binary(cmd)
        checks.append(
            PreflightCheck(
                name=f"{cmd} available",
                ok=bool(binary),
                details=binary or f"{cmd} not found in PATH or common system paths",
            )
        )

    checks.append(
        PreflightCheck(
            name="/dev/kvm present",
            ok=Path("/dev/kvm").exists(),
            details="Required for hardware acceleration",
        )
    )
    checks.append(
        PreflightCheck(
            name="Root privileges",
            ok=_is_root(),
            details="Current UID must be root (uid=0) for full workflow",
        )
    )
    return checks
