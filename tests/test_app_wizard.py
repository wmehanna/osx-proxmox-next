import asyncio
from pathlib import Path

from osx_proxmox_next import app as app_module
from osx_proxmox_next.app import NextApp
from osx_proxmox_next.executor import ApplyResult


def test_wizard_starts_with_guided_status() -> None:
    async def _run() -> None:
        app = NextApp()
        async with app.run_test(size=(90, 28)) as pilot:
            await pilot.click("#nav_wizard")
            assert (
                "Step 1" in app.wizard_status_text
                or "Preflight has failures" in app.wizard_status_text
            )

    asyncio.run(_run())


def test_apply_dry_does_not_create_snapshot(monkeypatch) -> None:
    calls = {"snapshots": 0}

    def fake_snapshot(_vmid: int):
        calls["snapshots"] += 1
        raise AssertionError("dry apply must not snapshot")

    def fake_apply_plan(steps, execute=False, on_step=None, adapter=None):  # type: ignore[no-untyped-def]
        for idx, step in enumerate(steps, start=1):
            if on_step:
                on_step(idx, len(steps), step, None)
                class _R:
                    ok = True
                    returncode = 0
                on_step(idx, len(steps), step, _R())
        return ApplyResult(ok=True, results=[], log_path=Path("/tmp/fake.log"))

    monkeypatch.setattr(app_module, "create_snapshot", fake_snapshot)
    monkeypatch.setattr(app_module, "apply_plan", fake_apply_plan)

    async def _run() -> None:
        app = NextApp()
        async with app.run_test(size=(90, 28)) as pilot:
            await pilot.click("#nav_wizard")
            app.preflight_has_run = True
            await pilot.press("a")
            await pilot.pause()
            await pilot.pause()

    asyncio.run(_run())
    assert calls["snapshots"] == 0


def test_use_recommended_populates_empty_fields() -> None:
    async def _run() -> None:
        app = NextApp()
        async with app.run_test(size=(120, 44)) as pilot:
            await pilot.click("#nav_wizard")
            await pilot.click("#goto_step2")
            app.query_one("#vmid").value = ""
            app.query_one("#name").value = ""
            app.query_one("#macos").value = ""
            await pilot.click("#defaults")
            await pilot.pause()
            assert app.query_one("#vmid").value.strip() == "900"
            assert app.query_one("#name").value.strip() == "macos-sequoia"
            assert app.query_one("#macos").value.strip() == "sequoia"

    asyncio.run(_run())


def test_locked_fields_and_storage_quick_select() -> None:
    async def _run() -> None:
        app = NextApp()
        async with app.run_test(size=(120, 44)) as pilot:
            await pilot.click("#nav_wizard")
            await pilot.click("#goto_step2")
            assert app.query_one("#macos").disabled is True
            await pilot.click("#toggle_advanced")
            assert app.query_one("#cores").disabled is True
            await pilot.click("#back_basic")
            await pilot.click("#storage_pick_0")
            assert app.query_one("#storage").value.strip() != ""

    asyncio.run(_run())


def test_invalid_form_blocks_step3_navigation() -> None:
    async def _run() -> None:
        app = NextApp()
        async with app.run_test(size=(120, 44)) as pilot:
            await pilot.click("#nav_wizard")
            await pilot.click("#goto_step2")
            app.query_one("#vmid").value = "abc"
            await pilot.click("#goto_step3")
            await pilot.pause()
            assert app.step_page == 2
            assert app.query_one("#vmid").has_class("invalid")
            assert "Fix highlighted fields" in app.wizard_status_text

    asyncio.run(_run())


def test_use_recommended_uses_next_available_vmid(monkeypatch) -> None:
    monkeypatch.setattr(NextApp, "_detect_next_vmid", lambda self: 1234)

    async def _run() -> None:
        app = NextApp()
        async with app.run_test(size=(120, 44)) as pilot:
            await pilot.click("#nav_wizard")
            await pilot.click("#goto_step2")
            await pilot.click("#defaults")
            await pilot.pause()
            assert app.query_one("#vmid").value.strip() == "1234"

    asyncio.run(_run())
