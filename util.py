from typing import List


def cumulative_sum(sequence: List[int]) -> List[int]:
    """Naive implementation of cumulative sum."""

    retval = []
    for idx in range(1, len(sequence) + 1):
        retval.append(sum(sequence[:idx]))
    return retval
