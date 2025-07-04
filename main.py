import pyautogui
import time
from PIL import Image
import pytesseract
import ctypes
from typing import Tuple

BOOK_PIXEL_COLOR = (100, 74, 23)
FIRST_OFFER_PIXEL_TO_CHECK = (606, 329)
SECOND_OFFER_PIXEL_TO_CHECK = (606, 410)

SLEEP_DURATION_FOR_UI_UPDATES = 0.5
SECONDS_TO_BREAK_LECTERN = 0.5

FIRST_OFFER_TARGET_PIXEL = (735, 329)
SECOND_OFFER_TARGET_PIXEL = (735, 410)

FIRST_OFFER_BOOK_TOP_LEFT = (767, 315)
FIRST_OFFER_BOOK_BOTTOM_RIGHT = (1312, 365)
SECOND_TARGET_BOOK_TOP_LEFT = (767, 402)
SECOND_TARGET_BOOK_BOTTOM_RIGHT = (1312, 452)

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP   = 0x0004


pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'


class MouseInputStruct(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class InputUnion(ctypes.Structure):
    _fields_ = [
        ("type", ctypes.c_ulong),
        ("mi", MouseInputStruct)
    ]


def get_screen_capture(top_left: Tuple[int, int], bottom_right: Tuple[int, int]) -> Image:
    x1, y1 = top_left
    x2, y2 = bottom_right
    return pyautogui.screenshot(region=(x1, y1, x2 - x1, y2 - y1))


def get_text_from_image(image: Image) -> str:
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
    first_offer_image = get_screen_capture(FIRST_OFFER_BOOK_TOP_LEFT, FIRST_OFFER_BOOK_BOTTOM_RIGHT)
    return get_text_from_image(first_offer_image)


def get_second_offer_enchantment() -> str:
    pyautogui.moveTo(*SECOND_OFFER_TARGET_PIXEL)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)
    second_offer_image = get_screen_capture(SECOND_TARGET_BOOK_TOP_LEFT, SECOND_TARGET_BOOK_BOTTOM_RIGHT)
    return get_text_from_image(second_offer_image)


def exit_trading_dialog() -> None:
    pyautogui.press('escape')
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)


def look_at_job_block_from_villager() -> None:
    pyautogui.move(0, 60, duration=0.5)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)


def look_at_villager_from_block() -> None:
    pyautogui.move(0, -60, duration=0.5)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)


def perform_left_mouse_click(click_hold_duration: float) -> None:
    send_input = ctypes.windll.user32.SendInput
    extra_info = ctypes.c_ulong(0)
    input_structure = InputUnion()
    input_structure.type = 0
    input_structure.mi = MouseInputStruct(
        0, 0, 0, MOUSEEVENTF_LEFTDOWN, 0, ctypes.pointer(extra_info)
    )
    send_input(1, ctypes.pointer(input_structure), ctypes.sizeof(input_structure))

    time.sleep(click_hold_duration)

    input_structure.mi = MouseInputStruct(
        0, 0, 0, MOUSEEVENTF_LEFTUP, 0, ctypes.pointer(extra_info)
    )
    send_input(1, ctypes.pointer(input_structure), ctypes.sizeof(input_structure))


def break_block_ahead() -> None:
    perform_left_mouse_click(SECONDS_TO_BREAK_LECTERN)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)


def place_lectern() -> None:
    pyautogui.rightClick()


def open_villager_trading_dialog() -> None:
    pyautogui.click(button='right', duration=0.1)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)


def get_new_offer() -> None:
    exit_trading_dialog()
    look_at_job_block_from_villager()
    break_block_ahead()
    place_lectern()
    look_at_villager_from_block()
    open_villager_trading_dialog()    
    

def main():
    time.sleep(4)

    while True:
        print("Checking for enchanted book offers...")
        if is_first_offer_book():
            print("First offer is a book with text:", get_first_offer_enchantment())
        elif is_second_offer_book():
            print("Second offer is a book with text:", get_second_offer_enchantment())
        else:
            print("No enchanted book offer found.")
            get_new_offer()

if __name__ == "__main__":
    main()
