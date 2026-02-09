from osx_proxmox_next.diagnostics import build_health_status, recovery_guide


def test_recovery_guide_contains_core_steps() -> None:
    lines = recovery_guide("boot failed")
    assert any("Preflight" in line or "preflight" in line for line in lines)


def test_health_status_has_counts() -> None:
    status = build_health_status()
    assert status.total >= status.score
