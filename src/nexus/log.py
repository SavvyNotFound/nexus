import sys
from typing import Never


def LogCore(value: str):
    print(f"[nexus]: {value}")


def PrintNexusUsage():
    LogCore("Invalid use of application!")


def AssertTrue(value: str) -> Never:
    LogCore(value)
    sys.exit()
    return Never
