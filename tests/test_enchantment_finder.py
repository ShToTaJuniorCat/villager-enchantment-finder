import pytest
from src.enchantments_finder import _does_enchantment_match_target, _does_name_match_target, _does_level_match_target, is_enchantment_a_target


@pytest.mark.parametrize(
    "enchantment_name, target, expected",
    [
        ("Aqua Affinity", {"name": "aqua affinity", "level": "", "common_ocr_errors": []}, True),
        ("Aqua Attinity", {"name": "aqua affinity", "level": "", "common_ocr_errors": ["aqua attinity"]}, True),
        ("aqua affinity", {"name": "aqua affinity", "level": "", "common_ocr_errors": []}, True),
        ("mend1ng", {"name": "mending", "level": "", "common_ocr_errors": ["mend1ng"]}, True),
        ("mending", {"name": "mending", "level": "iv", "common_ocr_errors": []}, True),
        ("Sharpness", {"name": "mending", "level": "", "common_ocr_errors": ["mend1ng", "mend!ng"]}, False),
    ],
)
def test_does_name_match_target(enchantment_name, target, expected):
    result = _does_name_match_target(enchantment_name, target)
    assert (
        result == expected
    ), f"Expected {expected} but got {result} for {enchantment_name} against target {target}"


@pytest.mark.parametrize(
    "enchantment_level, target, expected",
    [
        ("", {"name": "aqua affinity", "level": "", "common_ocr_errors": []}, True),
        ("iii", {"name": "unbreaking", "level": "iii", "common_ocr_errors": []}, True),
        ("iv", {"name": "protection", "level": "iv", "common_ocr_errors": []}, True),
        ("i\\", {"name": "protection", "level": "iv", "common_ocr_errors": []}, True),
        ("!\\|", {"name": "protection", "level": "iv", "common_ocr_errors": []}, True),
        ("i", {"name": "mending", "level": "", "common_ocr_errors": []}, False),
        ("ii|", {"name": "protection", "level": "iv", "common_ocr_errors": []}, False),
    ],
)
def test_does_level_match_target(enchantment_level, target, expected):
    result = _does_level_match_target(enchantment_level, target)
    assert (
        result == expected
    ), f"Expected {expected} but got {result} for level {enchantment_level} against target {target}"


@pytest.mark.parametrize(
    "enchantment_name, enchantment_level, target, expected",
    [
        ("Aqua Affinity", "", {"name": "aqua affinity", "level": "", "common_ocr_errors": ["aqua attinity"]}, True),
        ("Unbreaking", "III", {"name": "unbreaking", "level": "iii", "common_ocr_errors": []}, True),
        ("mending", "", {"name": "mending", "level": "", "common_ocr_errors": []}, True),
        ("Aqua Attinity", "", {"name": "aqua affinity", "level": "", "common_ocr_errors": ["aqua attinity"]}, True),
        ("Aqua Affinity", "", {"name": "aqua affinity", "level": "", "common_ocr_errors": []}, True),
        ("Mending", "", {"name": "mending", "level": "", "common_ocr_errors": []}, True),
        ("mending", "", {"name": "mending", "level": "", "common_ocr_errors": []}, True),
        ("mend1ng", "", {"name": "mending", "level": "", "common_ocr_errors": ["mend1ng"]}, True),
        ("protection", "ii|", {"name": "protection", "level": "iv", "common_ocr_errors": []}, False),
        ("mending", "i", {"name": "mending", "level": "", "common_ocr_errors": []}, False),
        ("unbreaking", "i", {"name": "unbreaking", "level": "iii", "common_ocr_errors": []}, False),
    ],
)
def test_does_enchantment_match_target(
    enchantment_name, enchantment_level, target, expected
):
    result = _does_enchantment_match_target(enchantment_name, enchantment_level, target)
    assert (
        result == expected
    ), f"Expected {expected} but got {result} for {enchantment_name} {enchantment_level} against target {target}"


@pytest.mark.parametrize(
    "enchantment, targets, expected",
    [
        ("Aqua Affinity", [{"name": "aqua affinity", "level": "", "common_ocr_errors": []}], True),
    ],
)
def test_is_enchantment_a_target(enchantment, targets, expected):
    result = is_enchantment_a_target(enchantment, targets)
    assert (
        result == expected
    ), f"Expected {expected} but got {result} for enchantment {enchantment} against targets {targets}"