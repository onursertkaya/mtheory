"""Common constants."""
from typing import List

SHARP = "#"
FLAT = "b"
NATURAL = list("ABCDEFG")
CHROMATIC = sorted([q + SHARP for q in NATURAL if q not in "BE"] + NATURAL)


class Color:
    """Color codes for terminal output."""

    # pylint: disable=too-few-public-methods

    RESET = "\033[0m"
    BOLD = "\033[1m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"

    BOLDRED = f"{BOLD}{RED}"
    BOLDGREEN = f"{BOLD}{GREEN}"
    BOLDYELLOW = f"{BOLD}{YELLOW}"
    BOLDBLUE = f"{BOLD}{BLUE}"


INTERVAL_SHORTNAMES = (
    " Ro ",
    "min2",
    "maj2",
    "min3",
    "maj3",
    " p4 ",
    " Tr ",
    " p5 ",
    "min6",
    "maj6",
    "min7",
    "maj7",
)


def get_short_name_by_degree(degree: int):
    """Get the short name of an interval by degree.

    E.g.
    0 -> Ro (root)
    1 -> min2 (minor second)
    2 -> maj2 (major second)
    ...
    """
    return INTERVAL_SHORTNAMES[degree % len(INTERVAL_SHORTNAMES)]


def rearrange_chromatic_by_root(root_name: str) -> List[str]:
    """Cycle chromatic symbols with root at start position."""
    return _rearrange_by_root(root_name, CHROMATIC)


def rearrange_natural_by_root(root_name: str) -> List[str]:
    """Cycle natural symbols with root at start position."""
    return _rearrange_by_root(root_name, NATURAL)


def _rearrange_by_root(root_name: str, sequence: List[str]) -> List[str]:
    assert root_name in sequence
    start_note_idx = sequence.index(root_name)
    return sequence[start_note_idx:] + sequence[:start_note_idx]
