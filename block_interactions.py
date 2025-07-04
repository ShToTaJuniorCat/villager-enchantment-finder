import time
import ctypes

import pyautogui

from consts import SLEEP_DURATION_FOR_UI_UPDATES

SECONDS_TO_BREAK_LECTERN = 0.5

MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004


class MouseInputStruct(ctypes.Structure):
    _fields_ = [
        ("dx", ctypes.c_long),
        ("dy", ctypes.c_long),
        ("mouseData", ctypes.c_ulong),
        ("dwFlags", ctypes.c_ulong),
        ("time", ctypes.c_ulong),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong)),
    ]


class InputUnion(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong), ("mi", MouseInputStruct)]


def look_at_job_block_from_villager() -> None:
    pyautogui.move(0, 60, duration=0.5)
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
