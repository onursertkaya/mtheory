"""Fretboard representation."""
from typing import Type

from constants import CHROMATIC, INTERVAL_SHORTNAMES, Color, rearrange_chromatic_by_root
from mode import Mode
from scale import Scale
from util import cumulative_sum

FRET_TPL = "|--{}--"


class FretBoardPrint:
    """Fretboard representation for notes and intervals."""

    # TODO: use types instead of string matching while highlighting.

    TUNING = [0, 5, -5, 5, 5, 5, 4, 5]
    SIX_STRING = ["E", "A", "D", "G", "B", "E"]
    EIGHT_STRING = ["F#", "B", *SIX_STRING]
    FINGER_EXTENT = 5

    @staticmethod
    def notes():
        """Print fretboard with notes."""
        print(FretBoardPrint._notes())

    @staticmethod
    def degrees():
        """Print fretboard with degrees relative to tonic."""
        print(FretBoardPrint._frets())

    @staticmethod
    def highlight_degrees(scale_type: Type[Scale], mode: Mode):
        """Highlight degrees of a given scale and mode combination."""
        scale_interval_names = scale_type().degrees(mode)
        pretty_fret = FretBoardPrint._frets()
        pretty_fret_colorized = pretty_fret
        for short_name in scale_interval_names:
            color = Color.BOLDBLUE if short_name == INTERVAL_SHORTNAMES[0] else Color.BOLDRED
            pretty_fret_colorized = pretty_fret_colorized.replace(
                short_name, f"{color}{short_name}{Color.RESET}"
            )
        print(pretty_fret_colorized)

    @staticmethod
    def highlight_notes(scale: Scale, mode: Mode):
        """Highlight notes of a given scale and mode combination."""
        scale_note_names = [note.name for note in scale.notes(mode)]
        pretty_fret = FretBoardPrint._notes()
        pretty_fret_colorized = pretty_fret
        for name in scale_note_names:
            color = Color.BOLDBLUE if name == scale_note_names[0] else Color.BOLDRED
            pretty_fret_colorized = pretty_fret_colorized.replace(
                f" {name} ", f" {color}{name}{Color.RESET} "
            )
        print(pretty_fret_colorized)

    @staticmethod
    def _notes():
        retval = ""
        for idx, note_name in enumerate(reversed(FretBoardPrint.EIGHT_STRING)):
            rearranged_chromatic = rearrange_chromatic_by_root(note_name)
            two_octaves = 2 * [f" {q:^2}" for q in rearranged_chromatic]
            retval += f"{idx} " + "".join([FRET_TPL.format(n) for n in two_octaves]) + "|\n"
        retval += (
            "\n- " + "".join([FRET_TPL.format(f"{q:^3}") for q in range(len(two_octaves))]) + "|"
        )
        return retval

    @staticmethod
    def _frets() -> str:
        retval = ""
        for string_interval in reversed(cumulative_sum(FretBoardPrint.TUNING)):
            string_interval = string_interval % len(CHROMATIC)
            rearranged = (
                INTERVAL_SHORTNAMES[string_interval:] + INTERVAL_SHORTNAMES[:string_interval]
            )
            extend_left_to_right = (
                rearranged[-FretBoardPrint.FINGER_EXTENT :]
                + rearranged[: FretBoardPrint.FINGER_EXTENT + 1]
            )
            row_str = "".join([FRET_TPL.format(n) for n in extend_left_to_right]) + "|"
            retval += f"{row_str}\n"
        retval += (
            "".join(
                [
                    FRET_TPL.format(f"{q:^4}")
                    for q in range(-FretBoardPrint.FINGER_EXTENT, FretBoardPrint.FINGER_EXTENT + 1)
                ]
            )
            + "|"
            + "\n"
        )
        return retval
