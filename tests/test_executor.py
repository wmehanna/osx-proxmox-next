from osx_proxmox_next.executor import apply_plan
from osx_proxmox_next.planner import PlanStep


def test_apply_plan_dry_run_creates_success_results() -> None:
    steps = [PlanStep(title="Echo", argv=["echo", "hello"])]
    result = apply_plan(steps, execute=False)
    assert result.ok is True
    assert result.results[0].ok is True
    assert result.log_path.exists()
