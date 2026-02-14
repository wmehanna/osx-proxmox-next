from osx_proxmox_next.amd_patches import (
    _CORE_BYTE_OFFSET,
    _CORE_PATCH_COUNT,
    _PATCHES,
    get_kernel_patches,
    serialize_patches,
)


def test_patch_count() -> None:
    assert len(_PATCHES) == 25


def test_core_count_injection_default() -> None:
    patches = get_kernel_patches(8)
    for i in range(_CORE_PATCH_COUNT):
        assert patches[i]["Replace"][_CORE_BYTE_OFFSET] == 8


def test_core_count_injection_various() -> None:
    for cores in (1, 4, 16, 32, 64, 128):
        patches = get_kernel_patches(cores)
        for i in range(_CORE_PATCH_COUNT):
            assert patches[i]["Replace"][_CORE_BYTE_OFFSET] == cores


def test_core_count_does_not_mutate_originals() -> None:
    original_byte = _PATCHES[0]["Replace"][_CORE_BYTE_OFFSET]
    get_kernel_patches(42)
    assert _PATCHES[0]["Replace"][_CORE_BYTE_OFFSET] == original_byte


def test_non_core_patches_unchanged() -> None:
    patches_4 = get_kernel_patches(4)
    patches_8 = get_kernel_patches(8)
    for i in range(_CORE_PATCH_COUNT, len(patches_4)):
        assert patches_4[i] == patches_8[i]


def test_all_patches_have_required_keys() -> None:
    required = {"Find", "Replace", "Identifier", "MinKernel", "MaxKernel", "Enabled"}
    patches = get_kernel_patches(4)
    for i, p in enumerate(patches):
        missing = required - set(p.keys())
        assert not missing, f"Patch {i} ({p.get('Comment', '?')}) missing keys: {missing}"


def test_serialize_roundtrip() -> None:
    serialized = serialize_patches(8)
    result = eval(serialized)  # noqa: S307 — intentional, testing our own output
    assert isinstance(result, list)
    assert len(result) == 25
    assert result[0]["Replace"][_CORE_BYTE_OFFSET] == 8


def test_serialize_produces_valid_python() -> None:
    serialized = serialize_patches(4)
    compile(serialized, "<test>", "eval")
