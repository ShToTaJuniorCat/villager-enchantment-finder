import time
from typing import Tuple
import os

import pyautogui
from PIL import Image
import pytesseract

from consts import SLEEP_DURATION_FOR_UI_UPDATES

BOOK_PIXEL_COLOR = (100, 74, 23)
FIRST_OFFER_PIXEL_TO_CHECK = (606, 329)
SECOND_OFFER_PIXEL_TO_CHECK = (606, 410)

FIRST_OFFER_TARGET_PIXEL = (735, 329)
SECOND_OFFER_TARGET_PIXEL = (735, 410)

FIRST_OFFER_BOOK_TOP_LEFT = (767, 315)
FIRST_OFFER_BOOK_BOTTOM_RIGHT = (1312, 365)
SECOND_TARGET_BOOK_TOP_LEFT = (767, 402)
SECOND_TARGET_BOOK_BOTTOM_RIGHT = (1312, 452)
TARGET_ENCHANTEMTS = (
    "aqua affinity",
    "mending",
    "protection iv",
    "sharpness v",
    "unbreaking iii",
    "efficiency v",
    "fortune iii",
    "silk touch",
    "looting iii",
    "power v",
    "respiration iii",
    "depth strider iii",
    "feather falling iv",
)


pytesseract.pytesseract.tesseract_cmd = os.environ.get(
    "TESSERACT_CMD_PATH", r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)


def _get_screen_capture(
    top_left: Tuple[int, int], bottom_right: Tuple[int, int]
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


def is_enchantment_a_target(enchantment: str) -> bool:
    enchantment = enchantment.lower().strip()
    
    for target in TARGET_ENCHANTEMTS:
        if target.lower() in enchantment or enchantment in target.lower():
            return True
    
    return False