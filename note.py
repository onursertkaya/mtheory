"""Notes and steps."""
from __future__ import annotations

from enum import IntEnum
from typing import List


class Step(IntEnum):
    """Step between notes.

    Whole, half and whole+half.
    """

    H = 1
    W = 2
    WH = 3


class Note(IntEnum):
    """Enumeration for notes.

    Only represented with sharps, using *s suffix.
    """

    # pylint: disable=invalid-name
    A = 0
    As = 1
    B = 2
    C = 3
    Cs = 4
    D = 5
    Ds = 6
    E = 7
    F = 8
    Fs = 9
    G = 10
    Gs = 11

    @staticmethod
    def all() -> List[str]:
        """Get all note names."""
        return [k for k, v in Note.__dict__.items() if isinstance(v, int)]

    def next(self, step: Step) -> Note:
        """Get next note with step."""
        idx = (self + step) % (len(list(self.__class__)))
        return list(self.__class__)[idx]

    def prev(self, step: Step) -> Note:
        """Get previoous note by step."""
        idx = (self - step) % (len(list(self.__class__)))
        return list(self.__class__)[idx]
