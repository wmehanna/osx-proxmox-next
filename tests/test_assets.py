from pathlib import Path

from osx_proxmox_next.assets import required_assets, suggested_fetch_commands
from osx_proxmox_next.domain import VmConfig


def test_required_assets_respects_installer_path() -> None:
    cfg = VmConfig(
        vmid=900,
        name="macos-tahoe",
        macos="tahoe",
        cores=8,
        memory_mb=16384,
        disk_gb=160,
        bridge="vmbr0",
        storage="local-lvm",
        installer_path="/tmp/tahoe.iso",
    )
    checks = required_assets(cfg)
    assert any(c.path == Path("/tmp/tahoe.iso") for c in checks)


def test_suggested_fetch_commands_include_tahoe_note() -> None:
    cfg = VmConfig(
        vmid=900,
        name="macos-tahoe",
        macos="tahoe",
        cores=8,
        memory_mb=16384,
        disk_gb=160,
        bridge="vmbr0",
        storage="local-lvm",
        installer_path="",
    )
    cmds = suggested_fetch_commands(cfg)
    assert any("Tahoe" in c for c in cmds)
