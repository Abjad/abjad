import py.test
from fractions import Fraction
from experimental import quantizationtools


def test_quantizationtools_QGrid___new___01():
    '''The first argument is the "definition":
    a list whose length is prime, which can contain
    Numbers, QEvents, Nones, empty tuples, tuples of Numbers,
    tuples of QEvents, or more list following the same pattern.
    '''

    # numbers
    q = quantizationtools.QGrid([0, 0.5, Fraction(1, 4)], 0)

    # None, QEvent, empty tuple
    p = quantizationtools.QGrid([None, quantizationtools.PitchedQEvent(0, [0]), tuple([])], 0)

    # nested lists
    r = quantizationtools.QGrid([[0, 1], 2], 3)

    # tuple of QEvents
    s = quantizationtools.QGrid([(quantizationtools.PitchedQEvent(0, [0]), quantizationtools.PitchedQEvent(1, [0]))], 0)

    # tuple of Numbers
    t = quantizationtools.QGrid([(0, 0.5, Fraction(-1, 4))], 0)
