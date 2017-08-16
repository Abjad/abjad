import abjad
import pytest


def test_scoretools_Tuplet_from_ratio_and_pair_01():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 2, 4)),
        abjad.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/7 {
            c'16
            c'8
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_02():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 1, 2, 4)),
        abjad.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
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


def test_scoretools_Tuplet_from_ratio_and_pair_03():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((-2, 3, 7)),
        abjad.NonreducedFraction(7, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 7/12 {
            r8
            c'8.
            c'4..
        }
        '''
        )

def test_scoretools_Tuplet_from_ratio_and_pair_04():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((7, 7, -4, -1)),
        abjad.NonreducedFraction(1, 4),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \times 16/19 {
            c'16..
            c'16..
            r16
            r64
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_05():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 2, 2)),
        abjad.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_06():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((2, 4, 4)),
        abjad.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_07():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((4, 8, 8)),
        abjad.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'4
            c'2
            c'2
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_08():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((8, 16, 16)),
        abjad.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'4
            c'2
            c'2
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_09():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((2, 4, 4)),
        abjad.NonreducedFraction(3, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'16
            c'8
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_10():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((2, 4, 4)),
        abjad.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 3/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_11():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((2, 4, 4)),
        abjad.NonreducedFraction(12, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_12():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((2, 4, 4)),
        abjad.NonreducedFraction(24, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'4
            c'2
            c'2
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_13():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 2, 2)),
        abjad.NonreducedFraction(6, 2),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'2
            c'1
            c'1
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_14():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 2, 2)),
        abjad.NonreducedFraction(6, 4),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'4
            c'2
            c'2
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_15():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 2, 2)),
        abjad.NonreducedFraction(6, 8),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'8
            c'4
            c'4
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_16():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 2, 2)),
        abjad.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        \tweak text #tuplet-number::calc-fraction-text
        \times 6/5 {
            c'16
            c'8
            c'8
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_17():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, -1, -1)),
        abjad.NonreducedFraction(3, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            r16
            r16
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_18():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 1, -1, -1)),
        abjad.NonreducedFraction(4, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
        r'''
        {
            c'16
            c'16
            r16
            r16
        }
        '''
        )


def test_scoretools_Tuplet_from_ratio_and_pair_19():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 1, 1, -1, -1)),
        abjad.NonreducedFraction(5, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
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


def test_scoretools_Tuplet_from_ratio_and_pair_20():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1, 1, 1, 1, -1, -1)),
        abjad.NonreducedFraction(6, 16),
        )

    assert format(tuplet) == abjad.String.normalize(
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


def test_scoretools_Tuplet_from_ratio_and_pair_21():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((1,)),
        abjad.NonreducedFraction(6, 16),
        )

    assert str(tuplet) == 'Container("c\'4.")'


def test_scoretools_Tuplet_from_ratio_and_pair_22():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((99,)),
        abjad.NonreducedFraction(6, 16),
        )

    assert str(tuplet) == 'Container("c\'4.")'


def test_scoretools_Tuplet_from_ratio_and_pair_23():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((-1,)),
        abjad.NonreducedFraction(6, 16),
        )

    assert str(tuplet) == "Container('r4.')"


def test_scoretools_Tuplet_from_ratio_and_pair_24():

    tuplet = abjad.Tuplet.from_ratio_and_pair(
        abjad.NonreducedRatio((-99,)),
        abjad.NonreducedFraction(6, 16),
        )

    assert str(tuplet) == "Container('r4.')"


def test_scoretools_Tuplet_from_ratio_and_pair_25():

    statement = 'Tuplet.from_ratio_and_pair'
    statement += '([0], (3, 16))'
    pytest.raises(Exception, statement)


def test_scoretools_Tuplet_from_ratio_and_pair_26():

    statement = 'Tuplet.from_ratio_and_pair'
    statement += '([1, 1, 0, 1], (3, 16))'
    pytest.raises(Exception, statement)
