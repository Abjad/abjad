"""
Enumerations.
"""

import enum


class Comparison(enum.Enum):
    """
    Enumeration of amount comparisons.
    """

    LESS = -1
    EXACT = 0
    MORE = 1


class Horizontal(enum.Enum):
    """
    Enumeration of horizontal alignments.
    """

    LEFT = -1
    MIDDLE = 0
    RIGHT = 1


class Vertical(enum.Enum):
    """
    Enumeration of vertical alignments.
    """

    DOWN = -1
    CENTER = 0
    UP = 1


CENTER = Vertical.CENTER
DOWN = Vertical.DOWN
EXACT = Comparison.EXACT
LEFT = Horizontal.LEFT
LESS = Comparison.LESS
MIDDLE = Horizontal.MIDDLE
MORE = Comparison.MORE
RIGHT = Horizontal.RIGHT
UP = Vertical.UP
