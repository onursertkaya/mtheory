"""Chords."""
import abc
import sys
from enum import IntEnum
from typing import List

from mode import Mode
from note import Note
from scale import Natural, Scale


class ChordComposition(IntEnum):
    """Composition policy of a chord.

    https://en.wiktionary.org/wiki/polyad
    """

    POWER = 0
    TRIAD = 1
    TETRAD = 2
    PENTAD = 3
    AUG = 4
    DIM = 5
    SHARP_9 = 6
    FLAT_9 = 7
    FLAT_13 = 8
    SUS_2 = 9
    SUS_4 = 10


# pylint: disable=too-few-public-methods


def pick_idxs(comp: ChordComposition):
    """Get indexes to pick from scale notes per chord composition."""
    cc = ChordComposition
    return {
        cc.POWER: (0, 4),
        cc.TRIAD: (0, 2, 4),
        cc.SUS_2: (0, 1, 4),
        cc.SUS_4: (0, 3, 4),
    }[comp]


class Chord(abc.ABC):
    """Collection of notes."""

    def __init__(self, root: Note, comp: ChordComposition):
        self._root = root
        self._comp = comp

    @abc.abstractmethod
    def notes(self) -> List[str]:
        """Get notes of chord."""

    def _notes(self, mode: Mode) -> List[str]:
        notes = Scale.convert_to_standard_naming(Natural(self._root).notes(mode))
        return [notes[idx] for idx in pick_idxs(self._comp)]


class Power(Chord):
    """Power chord."""

    def __init__(self, root: Note):
        super().__init__(root, comp=ChordComposition.POWER)

    def notes(self):
        return self._notes(mode=Mode.Ionian)


class Major(Chord):
    """Major chord."""

    def __init__(self, root: Note):
        super().__init__(root, comp=ChordComposition.TRIAD)

    def notes(self):
        return self._notes(mode=Mode.Ionian)


class Minor(Chord):
    """Minor chord."""

    def __init__(self, root: Note):
        super().__init__(root, comp=ChordComposition.TRIAD)

    def notes(self):
        return self._notes(mode=Mode.Aeolian)


class Sus2(Chord):
    """Sus2 chord."""

    def __init__(self, root: Note):
        super().__init__(root, comp=ChordComposition.SUS_2)

    def notes(self):
        return self._notes(mode=Mode.Ionian)


class Sus4(Chord):
    """Sus4 chord."""

    def __init__(self, root: Note):
        super().__init__(root, comp=ChordComposition.SUS_4)

    def notes(self):
        return self._notes(mode=Mode.Ionian)


def chord_names():
    """Get supported chord names."""
    return ["Minor", "Major", "Power", "Sus2", "Sus4"]


def get_chord_by_short_desc(desc: str) -> Chord:
    """Get chord with a root note set using short description.

    Raises:
        RuntimeError: If description is invalid.
    """
    # pylint: disable=raise-missing-from
    try:
        chord_type_name, note = desc.split(" ")
    except ValueError:
        raise RuntimeError(f"Invalid chord description: {desc}")

    chord_type = getattr(sys.modules[__name__], chord_type_name, None)
    if chord_type is None:
        raise RuntimeError(f"Invalid chord type: {chord_type_name}")

    note = note.replace("#", "s")  # todo: also support flats
    if note not in Note.all():
        raise RuntimeError(f"Invalid root note: {note}")

    return chord_type(getattr(Note, note.capitalize()))


class Maj7th(Chord):
    """Major seventh chord."""


class Min7th(Chord):
    """Minor seventh chord."""


class Dominant7th(Chord):
    """Dominant seventh chord."""


class Add9(Chord):
    """Add nine chord."""


class MinorAdd9(Chord):
    """Minor add nine chord."""


class Add11(Chord):
    """Add eleven chord."""


class MinorAdd11(Chord):
    """Minor add eleven chord."""


class Major6(Chord):
    """Major six chord."""


class Minor6(Chord):
    """Minor six chord."""
