import time

import pyautogui

from consts import SLEEP_DURATION_FOR_UI_UPDATES

DIALOG_EXIT_KEY = "escape"
DIALOG_TOP_LEFT_PIXEL = (435, 245)
DIALOG_BOTTOM_RIGHT_PIXEL = (1490, 865)
DIALOG_PIXELS_COLOR = (198, 198, 198)
SECONDS_TO_WAIT_FOR_DIALOG = 0.5


def exit_trading_dialog() -> None:
    pyautogui.press(DIALOG_EXIT_KEY, presses=1, interval=0.1)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)


def look_at_villager_from_block() -> None:
    pyautogui.move(0, -60, duration=0.5)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)


def _is_villager_dialog_open() -> bool:
    top_left_color = pyautogui.pixel(*DIALOG_TOP_LEFT_PIXEL)
    bottom_right_color = pyautogui.pixel(*DIALOG_BOTTOM_RIGHT_PIXEL)
    return (
        top_left_color == DIALOG_PIXELS_COLOR and
        bottom_right_color == DIALOG_PIXELS_COLOR
    )


def open_villager_trading_dialog() -> None:
    while not _is_villager_dialog_open():
        pyautogui.rightClick(duration=0.1)
        time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)
        time.sleep(SECONDS_TO_WAIT_FOR_DIALOG)
