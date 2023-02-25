"""Main program."""
from dataclasses import dataclass
from typing import Callable, Optional, Tuple

from chord import chord_names, get_chord_by_short_desc
from fretboard import FretBoardPrint
from mode import get_mode_by_shortname, mode_shortnames
from note import Note
from scale import Natural


def _print_modes():
    print(f"pick mode: {' | '.join(mode_shortnames())}")


def _print_chords():
    print(
        "pick chord type:\n"
        f"\t{' | '.join(chord_names())}\n"
        "and a note:\n"
        f"\t{', '.join(Note.all())}"
    )


@dataclass
class Command:
    """Command for the main program."""

    shorthand: str
    description: str
    fallback_func: Callable


COMMANDS = [
    Command("fn", "fretboard notes", FretBoardPrint.notes),
    Command("fd", "fretboard degrees", FretBoardPrint.degrees),
    Command("fi", "fretboard mode intervals", _print_modes),
    Command("c", "chords", _print_chords),
    Command("e", "exit", exit),
]


def _print_commands():
    print("commands:\n" + "\n".join([f"{cmd.shorthand} ({cmd.description})" for cmd in COMMANDS]))


def _get_user_input():
    request = input("> ")
    try:
        cmd, params = _parse_cmd(request)
        if cmd.shorthand == "fi":
            mode = get_mode_by_shortname(params)
            FretBoardPrint.highlight_degrees(Natural, mode)
        elif cmd.shorthand == "c":
            print(get_chord_by_short_desc(params).notes())
    except RuntimeError as err:
        print(err)
        return


def _parse_cmd(request: str) -> Tuple[Command, str]:
    params: Optional[str] = None
    if " " not in request:
        shorthand = request
    else:
        ws_idx = request.index(" ")
        shorthand, params = request[:ws_idx], request[ws_idx + 1 :]
    try:
        cmd = next(filter(lambda pick: pick.shorthand == shorthand, COMMANDS))
    except StopIteration:
        raise RuntimeError(f"Invalid usage: {request}")  # pylint: disable=raise-missing-from

    if params is None:
        cmd.fallback_func()
        raise RuntimeError()

    return cmd, params


if __name__ == "__main__":
    while True:
        _print_commands()
        _get_user_input()
