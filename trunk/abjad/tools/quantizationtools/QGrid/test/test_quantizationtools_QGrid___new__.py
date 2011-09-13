import py.test
from abjad import Fraction
from abjad.tools.quantizationtools import QEvent
from abjad.tools.quantizationtools import QGrid


def test_quantizationtools_QGrid___new___01():
    '''The first argument is the "definition":
    a list whose length is prime, which can contain
    Numbers, QEvents, Nones, empty tuples, tuples of Numbers,
    tuples of QEvents, or more list following the same pattern.
    '''

    # numbers
    q = QGrid([0, 0.5, Fraction(1, 4)], 0)

    # None, QEvent, empty tuple
    p = QGrid([None, QEvent(0, 0), tuple([])], 0)

    # nested lists
    r = QGrid([[0, 1], 2], 3)

    # tuple of QEvents
    s = QGrid([(QEvent(0, 0), QEvent(1, 0))], 0)

    # tuple of Numbers
    t = QGrid([(0, 0.5, Fraction(-1, 4))], 0)
