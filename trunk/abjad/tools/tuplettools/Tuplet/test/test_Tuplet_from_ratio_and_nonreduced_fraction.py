# -*- encoding: utf-8 -*-
from abjad import *
import py.test


# TODO: Port forward to new style of tests. #

# TEST TYPICAL DIVIDE #

def test_Tuplet_from_ratio_and_nonreduced_fraction_01():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 2, 4], (6, 16))
    assert str(tuplet) == "{@ 7:6 c'16, c'8, c'4 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_02():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 1, 2, 4], (6, 16))
    assert str(tuplet) == "{@ 4:3 c'16, c'16, c'8, c'4 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_03():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([-2, 3, 7], (7, 16))
    assert str(tuplet) == "{@ 12:7 r8, c'8., c'4.. @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_04():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([7, 7, -4, -1], (1, 4))
    assert str(tuplet) == "{@ 19:16 c'16.., c'16.., r16, r64 @}"


# TEST DIVIDE, DOUBLE LIST #

def test_Tuplet_from_ratio_and_nonreduced_fraction_05():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 2, 2], (12, 16))
    assert str(tuplet) == "{@ 5:6 c'8, c'4, c'4 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_06():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([2, 4, 4], (12, 16))
    assert str(tuplet) == "{@ 5:6 c'8, c'4, c'4 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_07():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([4, 8, 8], (12, 16))
    assert str(tuplet) == "{@ 5:3 c'4, c'2, c'2 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_08():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([8, 16, 16], (12, 16))
    assert str(tuplet) == "{@ 5:3 c'4, c'2, c'2 @}"


# TEST DIVIDE, DOUBLE NUMERATOR #

def test_Tuplet_from_ratio_and_nonreduced_fraction_09():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([2, 4, 4], (3, 16))
    assert str(tuplet) == "{@ 5:3 c'16, c'8, c'8 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_10():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([2, 4, 4], (6, 16))
    assert str(tuplet) == "{@ 5:3 c'8, c'4, c'4 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_11():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([2, 4, 4], (12, 16))
    assert str(tuplet) == "{@ 5:6 c'8, c'4, c'4 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_12():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([2, 4, 4], (24, 16))
    assert str(tuplet) == "{@ 5:6 c'4, c'2, c'2 @}"


# TEST DIVIDE, DOUBLE DENOMINATOR #

def test_Tuplet_from_ratio_and_nonreduced_fraction_13():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 2, 2], (6, 2))
    assert str(tuplet) == "{@ 5:6 c'2, c'1, c'1 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_14():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 2, 2], (6, 4))
    assert str(tuplet) == "{@ 5:6 c'4, c'2, c'2 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_15():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 2, 2], (6, 8))
    assert str(tuplet) == "{@ 5:6 c'8, c'4, c'4 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_16():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 2, 2], (6, 16))
    assert str(tuplet) == "{@ 5:6 c'16, c'8, c'8 @}"


# TEST DIVIDE, NO PROLATION #

def test_Tuplet_from_ratio_and_nonreduced_fraction_17():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, -1, -1], (3, 16))
    assert str(tuplet) == "{@ 1:1 c'16, r16, r16 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_18():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 1, -1, -1], (4, 16))
    assert str(tuplet) == "{@ 1:1 c'16, c'16, r16, r16 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_19():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 1, 1, -1, -1], (5, 16))
    assert str(tuplet) == "{@ 1:1 c'16, c'16, c'16, r16, r16 @}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_20():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1, 1, 1, 1, -1, -1], (6, 16))
    assert str(tuplet) == "{@ 1:1 c'16, c'16, c'16, c'16, r16, r16 @}"


# TEST LONE DIVIDE #

def test_Tuplet_from_ratio_and_nonreduced_fraction_21():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([1], (6, 16))
    assert str(tuplet) == "{c'4.}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_22():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([99], (6, 16))
    assert str(tuplet) == "{c'4.}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_23():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([-1], (6, 16))
    assert str(tuplet) == "{r4.}"

def test_Tuplet_from_ratio_and_nonreduced_fraction_24():
    tuplet = Tuplet.from_ratio_and_nonreduced_fraction([-99], (6, 16))
    assert str(tuplet) == "{r4.}"


# TEST DIVIDE ASSERTIONS #

def test_Tuplet_from_ratio_and_nonreduced_fraction_25():
    statement = 'Tuplet.from_ratio_and_nonreduced_fraction([], (3, 16))'
    py.test.raises(Exception, statement)

def test_Tuplet_from_ratio_and_nonreduced_fraction_26():
    statement = 'Tuplet.from_ratio_and_nonreduced_fraction([0], (3, 16))'
    py.test.raises(Exception, statement)

def test_Tuplet_from_ratio_and_nonreduced_fraction_27():
    statement = 'Tuplet.from_ratio_and_nonreduced_fraction([1, 1, 0, 1], (3, 16))'
    py.test.raises(Exception, statement)
