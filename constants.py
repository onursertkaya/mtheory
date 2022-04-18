SHARP = "#"
FLAT = "b"
NATURAL = [q for q in "ABCDEFG"]
CHROMATIC = sorted([q + SHARP for q in NATURAL if q not in "BE"] + NATURAL)


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
