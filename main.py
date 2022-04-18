from mode import (
    get_avaliable_scales,
    get_scale_by_shortname,
)
from fretboard import (
    FretBoard,
    FretIntervals,
)


def print_scales():
    print("pick scale: ", get_avaliable_scales())


COMMANDS = [
    ("f", "fretboard", FretBoard.print),
    ("s", "scale", print_scales),
    ("e", "exit", exit),
]


def print_commands():
    print(
        "commands:\n\t"
        + " | ".join([f"{shortcut} ({cmd})" for shortcut, cmd, _ in COMMANDS])
    )


def print_separator():
    sep = "\n" * 3
    print(sep, sep=None)


def get_user_input():
    req = input("> ")
    for sh, cmd, maybe_fun in COMMANDS:
        if req in [sh, cmd]:
            maybe_fun()
            return
        elif " " in req:
            try:
                scale_cmd, picked_scale = req.split(" ")
                assert scale_cmd == "s"
                FretIntervals.print_scale(get_scale_by_shortname(picked_scale).scale())
            except:
                print("usage: `f` OR `s [short_scale_name]` OR `e`")
            return


if __name__ == "__main__":

    while True:
        print_commands()
        get_user_input()
        print_separator()
