"""Scales."""
from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import List, Optional

from constants import FLAT, SHARP, get_short_name_by_degree, rearrange_natural_by_root
from mode import Mode
from note import Note, Step
from util import cumulative_sum


@dataclass(frozen=True)
class Scale(ABC):
    """Scale."""

    MAX_ACCIDENTAL_COUNT = 2
    PRINT_PADDING = 2

    root: Optional[Note] = None

    @staticmethod
    @abstractmethod
    def _aeolian_interval_pattern():
        pass

    def mode_interval_pattern(self, mode: Mode) -> List[Step]:
        """Intervals of the mode, relative to aeolian step pattern."""
        base = self._aeolian_interval_pattern()
        for _ in range(mode):
            base.append(base.pop(0))
        return base

    def notes(self, mode: Mode) -> List[Note]:
        """Notes of the scale."""
        assert self.root is not None, "Root must be set during init to be able to get scale notes."
        curr_note = self.root

        notes_ = []
        for tone in self.mode_interval_pattern(mode):
            notes_.append(curr_note)
            curr_note = curr_note.next(tone)
        return notes_

    def degrees(self, mode: Mode) -> List[str]:
        """Degree sequence of the scale."""
        sequence = self._cycle(mode.value)
        degrees = [0] + cumulative_sum(sequence)
        return [get_short_name_by_degree(i) for i in degrees]

    @staticmethod
    def convert_to_standard_naming(notes: List[Note]) -> List[str]:
        """Convert a sequence of notes to the standard naming.

        Standard naming dictates the existence of each non-accidental note in a
        scale. Based on the root note and the intervals,
        """
        names = [note.name for note in notes]
        all_naturalized = list(map(lambda name: name.strip("s"), names))
        duplicate_naturals_found = len(set(all_naturalized)) != len(names)
        if duplicate_naturals_found:
            fixed = []
            natural_rearranged = rearrange_natural_by_root(all_naturalized[0])
            for natural, naturalized, original_note in zip(
                natural_rearranged, all_naturalized, names
            ):
                if natural != naturalized:
                    diff = getattr(Note, original_note) - getattr(Note, natural)
                    diff = (
                        # prevent adding more than 2 accidentals by rotating the accidental
                        diff + len(Note.all())
                        if abs(diff) > Scale.MAX_ACCIDENTAL_COUNT
                        else diff
                    )
                    accidental_count = abs(diff)
                    accidental = "s" if diff > 0 else "b"

                    fixed.append(f"{natural}{accidental*accidental_count}")
                else:
                    fixed.append(original_note)
            out = fixed
        else:
            out = names

        total_padding = Scale.MAX_ACCIDENTAL_COUNT + 1 + 2 * Scale.PRINT_PADDING
        return [f"{note.replace('s', SHARP).replace('b', FLAT):^{total_padding}}" for note in out]

    def _cycle(self, times: int):
        seq = type(self)._aeolian_interval_pattern()
        return seq[times:] + seq[:times]


class Natural(Scale):
    """Natural scale."""

    @staticmethod
    def _aeolian_interval_pattern() -> List[Step]:
        t = Step
        return [t.W, t.H, t.W, t.W, t.H, t.W, t.W]


class Harmonic(Scale):
    """Harmonic scale."""

    @staticmethod
    def _aeolian_interval_pattern() -> List[Step]:
        t = Step
        return [t.W, t.H, t.W, t.W, t.H, t.WH, t.H]


class Melodic(Scale):
    """Melodic scale."""

    @staticmethod
    def _aeolian_interval_pattern() -> List[Step]:
        t = Step
        return [t.W, t.H, t.W, t.W, t.W, t.W, t.H]


def print_all():
    """Print all possible modes, intervals and notes."""
    print("Natural notes:")
    for note in Note.all():
        print(Natural(getattr(Note, note)).notes(Mode.Ionian))

    print("Harmonic notes:")
    for note in Note.all():
        print(Harmonic(getattr(Note, note)).notes(Mode.Ionian))

    print("Melodic notes:")
    for note in Note.all():
        print(Melodic(getattr(Note, note)).notes(Mode.Ionian))

    for mode in list(Mode):
        print(mode)
        print("Natural:")
        print(Natural().mode_interval_pattern(mode))
        print("Harmonic:")
        print(Harmonic().mode_interval_pattern(mode))
        print("Melodic:")
        print(Melodic().mode_interval_pattern(mode))
