import time

import pyautogui

from consts import SLEEP_DURATION_FOR_UI_UPDATES


def open_villager_trading_dialog() -> None:
    pyautogui.click(button="right", duration=0.1)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)


def exit_trading_dialog() -> None:
    pyautogui.press("escape")
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)


def look_at_villager_from_block() -> None:
    pyautogui.move(0, -60, duration=0.5)
    time.sleep(SLEEP_DURATION_FOR_UI_UPDATES)
