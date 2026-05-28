# paths.py  ← sits at project root
import os
import sys


def get_root() -> str:
    if getattr(sys, "frozen", False):
        return sys._MEIPASS
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
