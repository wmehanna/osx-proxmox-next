from osx_proxmox_next.domain import VmConfig
from osx_proxmox_next.profiles import get_profile, save_profile


def test_save_and_get_profile(monkeypatch, tmp_path) -> None:
    monkeypatch.setenv("HOME", str(tmp_path))
    cfg = VmConfig(
        vmid=900,
        name="macos-sequoia",
        macos="sequoia",
        cores=8,
        memory_mb=16384,
        disk_gb=128,
        bridge="vmbr0",
        storage="local-lvm",
        installer_path="",
    )
    save_profile("lab", cfg)
    loaded = get_profile("lab")
    assert loaded is not None
    assert loaded.name == "macos-sequoia"
