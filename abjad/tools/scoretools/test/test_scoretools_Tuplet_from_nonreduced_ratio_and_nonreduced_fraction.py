# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_01():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 2, 4)),
        mathtools.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/7 {
            c'16
            c'8
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_02():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 1, 2, 4)),
        mathtools.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/4 {
            c'16
            c'16
            c'8
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_03():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((-2, 3, 7)),
        mathtools.NonreducedFraction(7, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 7/12 {
            r8
            c'8.
            c'4..
        }
        '''
        )

def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_04():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((7, 7, -4, -1)),
        mathtools.NonreducedFraction(1, 4),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \times 16/19 {
            c'16..
            c'16..
            r16
            r64
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_05():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 2, 2)),
        mathtools.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_06():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((2, 4, 4)),
        mathtools.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_07():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((4, 8, 8)),
        mathtools.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'4
            c'2
            c'2
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_08():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((8, 16, 16)),
        mathtools.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'4
            c'2
            c'2
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_09():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((2, 4, 4)),
        mathtools.NonreducedFraction(3, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'16
            c'8
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_10():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((2, 4, 4)),
        mathtools.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_11():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((2, 4, 4)),
        mathtools.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_12():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((2, 4, 4)),
        mathtools.NonreducedFraction(24, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'4
            c'2
            c'2
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_13():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 2, 2)),
        mathtools.NonreducedFraction(6, 2),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'2
            c'1
            c'1
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_14():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 2, 2)),
        mathtools.NonreducedFraction(6, 4),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'4
            c'2
            c'2
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_15():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 2, 2)),
        mathtools.NonreducedFraction(6, 8),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_16():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 2, 2)),
        mathtools.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'16
            c'8
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_17():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, -1, -1)),
        mathtools.NonreducedFraction(3, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            r16
            r16
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_18():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 1, -1, -1)),
        mathtools.NonreducedFraction(4, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'16
            r16
            r16
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_19():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 1, 1, -1, -1)),
        mathtools.NonreducedFraction(5, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'16
            c'16
            r16
            r16
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_20():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1, 1, 1, 1, -1, -1)),
        mathtools.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == stringtools.normalize(
        r'''
        {
            c'16
            c'16
            c'16
            c'16
            r16
            r16
        }
        '''
        )


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_21():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((1,)),
        mathtools.NonreducedFraction(6, 16),
        )

    assert str(tuplet) == 'Container("c\'4.")'


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_22():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((99,)),
        mathtools.NonreducedFraction(6, 16),
        )

    assert str(tuplet) == 'Container("c\'4.")'


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_23():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((-1,)),
        mathtools.NonreducedFraction(6, 16),
        )

    assert str(tuplet) == "Container('r4.')"


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_24():

    tuplet = Tuplet.from_nonreduced_ratio_and_nonreduced_fraction(
        mathtools.NonreducedRatio((-99,)),
        mathtools.NonreducedFraction(6, 16),
        )

    assert str(tuplet) == "Container('r4.')"


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_25():

    statement = 'Tuplet.from_nonreduced_ratio_and_nonreduced_fraction'
    statement += '([0], (3, 16))'
    pytest.raises(Exception, statement)


def test_scoretools_Tuplet_from_nonreduced_ratio_and_nonreduced_fraction_26():

    statement = 'Tuplet.from_nonreduced_ratio_and_nonreduced_fraction'
    statement += '([1, 1, 0, 1], (3, 16))'
    pytest.raises(Exception, statement)
