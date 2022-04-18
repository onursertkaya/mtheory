H = 1  # half step
W = 2  # whole step

INTERVAL_SHORTNAMES = (
    " Ro ",
    "min2",
    "maj2",
    "min3",
    "maj3",
    " p4 ",
    " Tr ",
    " p5 ",
    "min6",
    "maj6",
    "min7",
    "maj7",
)

# Currently unused.
TWO_OCTAVE_INTERVAL_SHORT_NAMES = (
    *INTERVAL_SHORTNAMES,
    "octa",
    "min9",
    "maj9",
    "mi10",
    "ma10",
    " p11",
    "au11",  # a.k.a. dim12 / tritone-octave.
    " p12",
    "mi13",
    "ma13",
    "mi14",
    "ma14",
    " p15",
)


def get_short_name_by_degree(degree: int):
    return INTERVAL_SHORTNAMES[degree % len(INTERVAL_SHORTNAMES)]
