import time
import os

import pyautogui
from PIL import Image
import pytesseract
from itertools import product

from src.consts import SLEEP_DURATION_FOR_UI_UPDATES

BOOK_PIXEL_COLOR = (100, 74, 23)
FIRST_OFFER_PIXEL_TO_CHECK = (606, 329)
SECOND_OFFER_PIXEL_TO_CHECK = (606, 410)

FIRST_OFFER_TARGET_PIXEL = (735, 329)
SECOND_OFFER_TARGET_PIXEL = (735, 410)

FIRST_OFFER_BOOK_TOP_LEFT = (767, 315)
FIRST_OFFER_BOOK_BOTTOM_RIGHT = (1312, 365)
SECOND_TARGET_BOOK_TOP_LEFT = (767, 402)
SECOND_TARGET_BOOK_BOTTOM_RIGHT = (1312, 452)
TARGET_ENCHANTMENTS = (
    {"name": "aqua affinity", "level": "", "common_ocr_errors": ["aqua attinity"]},
    {"name": "mending", "level": "", "common_ocr_errors": []},
    {"name": "protection", "level": "iv", "common_ocr_errors": ["frotection"]},
    {"name": "sharpness", "level": "v", "common_ocr_errors": []},
    {"name": "unbreaking", "level": "iii", "common_ocr_errors": []},
    {"name": "efficiency", "level": "v", "common_ocr_errors": []},
    {"name": "fortune", "level": "iii", "common_ocr_errors": []},
    {"name": "silk touch", "level": "", "common_ocr_errors": []},
    {"name": "looting", "level": "iii", "common_ocr_errors": ["lootin", "lootingg"]},
    {"name": "power", "level": "v", "common_ocr_errors": ["fower"]},
    {
        "name": "respiration",
        "level": "ii",
        "common_ocr_errors": ["resperation", "resfiration"],
    },
    {"name": "depth strider", "level": "iii", "common_ocr_errors": ["defth strider"]},
    {"name": "feather falling", "level": "iv", "common_ocr_errors": []},
)
COMMON_i_OCR_ERRORS = ["l", "i", "1", "!", "j", "|", "t"]
COMMON_v_OCR_ERRORS = ["u", "\\|", "m", "\\"]
LEVELS_COMMON_OCR_ERRORS = {
    "": [],
    "i": COMMON_i_OCR_ERRORS,
    "ii": ["".join(p) for p in product(COMMON_i_OCR_ERRORS, repeat=2)],
    "iii": ["".join(p) for p in product(COMMON_i_OCR_ERRORS, repeat=3)],
    "iv": ["".join(p) for p in product(COMMON_i_OCR_ERRORS, COMMON_v_OCR_ERRORS)],
    "v": COMMON_v_OCR_ERRORS,
}


pytesseract.pytesseract.tesseract_cmd = os.environ.get(
    "TESSERACT_CMD_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def _get_screen_capture(
    top_left: tuple[int, int], bottom_right: tuple[int, int]
) -> Image:
    x1, y1 = top_left
    x2, y2 = bottom_right
    return pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))


def _get_text_from_image(image: Image) -> str:
    return pytesseract.image_to_string(image)


def is_first_offer_book() -> bool:
    first_offer_pixel = pyautogui.pixel(*FIRST_OFFER_PIXEL_TO_CHECK)
    return first_offer_pixel == BOOK_PIXEL_COLOR


def is_second_offer_book() -> bool:
    second_offer_pixel = pyautogui.pixel(*SECOND_OFFER_PIXEL_TO_CHECK)
    return second_offer_pixel == BOOK_PIXEL_COLOR


def get_first_offer_enchantment() -> str:
    pyautogui.moveTo(*FIRST_OFFER_TARGET_PIXEL)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)
    first_offer_image = _get_screen_capture(
        FIRST_OFFER_BOOK_TOP_LEFT, FIRST_OFFER_BOOK_BOTTOM_RIGHT
    )
    return _get_text_from_image(first_offer_image)


def get_second_offer_enchantment() -> str:
    pyautogui.moveTo(*SECOND_OFFER_TARGET_PIXEL)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)
    second_offer_image = _get_screen_capture(
        SECOND_TARGET_BOOK_TOP_LEFT, SECOND_TARGET_BOOK_BOTTOM_RIGHT
    )
    return _get_text_from_image(second_offer_image)


def _does_name_match_target(enchantment_name: str, target: dict) -> bool:
    target_name = target["name"].lower()

    if target_name == enchantment_name.lower():
        return True

    common_ocr_errors = target.get("common_ocr_errors", [])

    if enchantment_name.lower() == target_name:
        return True

    for error in common_ocr_errors:
        if error in enchantment_name.lower():
            return True

    return False


def _does_level_match_target(
    enchantment_level: str,
    target: dict,
    levels_common_ocr_errors: dict[str, list[str]] = LEVELS_COMMON_OCR_ERRORS,
) -> bool:
    target_level = target["level"].lower()
    if target_level == enchantment_level.lower():
        return True
    common_ocr_errors = levels_common_ocr_errors.get(target_level, [])
    if enchantment_level.lower() == target_level:
        return True
    for error in common_ocr_errors:
        if error in enchantment_level.lower():
            return True
    return False


def _does_enchantment_match_target(
    enchantment_name: str,
    enchantment_level: str,
    target: dict,
    levels_common_ocr_errors: dict[str, list[str]] = LEVELS_COMMON_OCR_ERRORS,
) -> bool:
    name_matches = _does_name_match_target(enchantment_name, target)
    level_matches = _does_level_match_target(
        enchantment_level, target, levels_common_ocr_errors
    )
    return name_matches and level_matches


def is_enchantment_a_target(
    enchantment: str,
    targets: tuple[dict, ...] = TARGET_ENCHANTMENTS,
    levels_common_ocr_errors: dict[str, list[str]] = LEVELS_COMMON_OCR_ERRORS,
) -> bool:
    enchantment_details = enchantment.split(" ")
    enchantment_name = enchantment_details[0].lower().strip()
    print(f"Checking enchantment: {enchantment_name}")
    enchantment_level = (
        enchantment_details[1].lower().strip() if len(enchantment_details) > 1 else ""
    )
    
    for target in targets:
        if _does_enchantment_match_target(
            enchantment_name, enchantment_level, target, levels_common_ocr_errors
        ):
            return True
    return False
