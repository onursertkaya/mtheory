"""Modes of a scale."""
from __future__ import annotations

from enum import IntEnum
from typing import List


class Mode(IntEnum):
    """Modes of a scale."""

    # pylint: disable=invalid-name

    Ionian = 2
    Dorian = 3
    Phrygian = 4
    Lydian = 5
    Mixolydian = 6
    Aeolian = 0
    Locrian = 1

    @staticmethod
    def all() -> List[str]:
        """Get all mode names."""
        return [k for k, v in Mode.__dict__.items() if isinstance(v, int)]


def mode_shortnames() -> List[str]:
    """Get mode shortnames.

    E.g.
    Ionion -> ion
    Dorian -> dor
    ...
    """
    return [_format_shortname(m) for m in Mode.all()]


def get_mode_by_shortname(short_name: str) -> Mode:
    """Get a mode by shortname.

    Raises:
        RuntimeError: If short_name does not correspond to a mode's shortname.
    """
    try:
        name = next(filter(lambda m: _format_shortname(m) == short_name, Mode.all()))
    except StopIteration:
        raise RuntimeError(f"Invalid shortname: {short_name}")  # pylint: disable=raise-missing-from
    return getattr(Mode, name)


def _format_shortname(long_name: str) -> str:
    return long_name[:3].lower()
