import abc
from typing import List

from intervals import get_short_name_by_degree
from util import cumulative_sum


H = 1
W = 2


class Mode(abc.ABC):
    @abc.abstractproperty
    def scale():
        pass

    @staticmethod
    def _cycle(interval_sequence: List[int], times: int):
        return interval_sequence[times:] + interval_sequence[:times]


class NaturalMode(Mode):

    MINOR_INTERVALS = [W, H, W, W, H, W, W]

    def __init__(self, degree: int):
        self._degree = degree

    def scale(self):
        sequence = Mode._cycle(NaturalMode.MINOR_INTERVALS, self._degree)
        intervals = [0] + cumulative_sum(sequence)
        interval_names = [get_short_name_by_degree(i) for i in intervals]
        return interval_names


AEOLIAN = NaturalMode(0)
LOCRIAN = NaturalMode(1)
IONIAN = NaturalMode(2)
DORIAN = NaturalMode(3)
PHRYGIAN = NaturalMode(4)
LYDIAN = NaturalMode(5)
MIXOLYDIAN = NaturalMode(6)

SCALE_SHORTNAMES = {
    "aeo": AEOLIAN,
    "loc": LOCRIAN,
    "ion": IONIAN,
    "dor": DORIAN,
    "phr": PHRYGIAN,
    "lyd": LYDIAN,
    "mxl": MIXOLYDIAN,
}


def get_avaliable_scales() -> None:
    return " | ".join(SCALE_SHORTNAMES.keys())


def get_scale_by_shortname(shortname: str) -> NaturalMode:
    return SCALE_SHORTNAMES[shortname]
