from osx_proxmox_next.cli import build_parser


def test_cli_parser_has_expected_commands() -> None:
    parser = build_parser()
    cmds = parser._subparsers._group_actions[0].choices  # type: ignore[attr-defined]
    assert "preflight" in cmds
    assert "plan" in cmds
    assert "apply" in cmds
    assert "bundle" in cmds
