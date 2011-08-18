from abjad.tools.intervaltreetools import *
from abjad.tools.intervaltreetools._make_test_intervals import _make_test_intervals
from abjad import Fraction
import py.test


def test_intervaltreetools_shift_aggregate_offset_to_rational_01():
    rational = 0
    tree = IntervalTree(_make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)

    assert tree.low == 0
    assert tree.magnitude == shifted.magnitude
    assert tree.low == shifted.low

def test_intervaltreetools_shift_aggregate_offset_to_rational_02():
    rational = Fraction(1, 2)
    tree = IntervalTree(_make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)

    assert tree.magnitude == shifted.magnitude
    assert tree.low != shifted.low
    assert shifted.low == rational

def test_intervaltreetools_shift_aggregate_offset_to_rational_03():
    rational = Fraction(-1, 2)
    tree = IntervalTree(_make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)

    assert tree.magnitude == shifted.magnitude
    assert tree.low != shifted.low
    assert shifted.low == rational

def test_intervaltreetools_shift_aggregate_offset_to_rational_04():
    rational = Fraction(-1, 2)
    tree = IntervalTree(_make_test_intervals())

    shifted = shift_aggregate_offset_by_rational(tree, rational)
    shifted = shift_aggregate_offset_by_rational(shifted, -1 * rational)

    assert tree.magnitude == shifted.magnitude
    assert tree.low == shifted.low
