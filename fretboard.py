from typing import List

from constants import (
    CHROMATIC,
    BOLDRED,
    BOLDBLUE,
    BOLDYELLOW,
    RESET,
)
from intervals import INTERVAL_SHORTNAMES
from util import cumulative_sum


class FretBoard:
    SIX_STRING = ["E", "A", "D", "G", "B", "E"]
    EIGHT_STRING = ["F#", "B", *SIX_STRING]

    fret_tpl = "|--{}--"

    @staticmethod
    def print():
        for string_idx, string in enumerate(reversed(FretBoard.EIGHT_STRING)):
            start_note_idx = CHROMATIC.index(string)
            rearranged_chromatic = (
                CHROMATIC[start_note_idx:] + CHROMATIC[:start_note_idx]
            )
            rearranged_chromatic = [f" {q:^2}" for q in rearranged_chromatic]
            two_octaves = rearranged_chromatic + rearranged_chromatic
            print(
                f"{string_idx} "
                + "".join([FretBoard.fret_tpl.format(n) for n in two_octaves])
                + "|"
            )
        print(
            "\n- "
            + "".join(
                [
                    FretBoard.fret_tpl.format(f"{q:^3}")
                    for q in range(2 * len(rearranged_chromatic))
                ]
            )
            + "|"
        )


class FretIntervals:

    TUNING = [0, 5, 5, 5, 5, 5, 4, 5]
    fret_tpl = "|--{}--"

    finger_extent = 5

    @staticmethod
    def pretty_fret() -> str:
        retval = ""
        for string_interval in reversed(cumulative_sum(FretIntervals.TUNING)):
            string_interval = string_interval % len(CHROMATIC)
            rearranged = (
                INTERVAL_SHORTNAMES[string_interval:]
                + INTERVAL_SHORTNAMES[:string_interval]
            )
            extend_left_to_right = (
                rearranged[-FretIntervals.finger_extent :]
                + rearranged[: FretIntervals.finger_extent + 1]
            )
            row_str = (
                "".join(
                    [FretIntervals.fret_tpl.format(n) for n in extend_left_to_right]
                )
                + "|"
            )
            retval += f"{row_str}\n"
        return retval

    @staticmethod
    def pretty_fret_numbers() -> str:
        return (
            "".join(
                [
                    FretIntervals.fret_tpl.format(f"{q:^4}")
                    for q in range(
                        -FretIntervals.finger_extent, FretIntervals.finger_extent + 1
                    )
                ]
            )
            + "|"
            + "\n"
        )

    @staticmethod
    def print():
        print(FretIntervals.pretty_fret())
        print()
        print(f"{BOLDYELLOW}{FretIntervals.pretty_fret_numbers()}{RESET}")

    @staticmethod
    def print_scale(scale_interval_names: List[str]):
        pretty_fret = FretIntervals.pretty_fret()
        pretty_fret_colorized = pretty_fret
        for short_name in scale_interval_names:
            color = BOLDBLUE if short_name == INTERVAL_SHORTNAMES[0] else BOLDRED
            pretty_fret_colorized = pretty_fret_colorized.replace(
                short_name, f"{color}{short_name}{RESET}"
            )
        print(pretty_fret_colorized)
