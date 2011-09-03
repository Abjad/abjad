from abjad import *


def test_Tuplet_01():
    '''Init typical fmtuplet.'''

    u = Tuplet(Fraction(2, 3), Note(0, (1, 8)) * 3)
    assert repr(u) == "Tuplet(2/3, [c'8, c'8, c'8])"
    assert str(u) == "{* 3:2 c'8, c'8, c'8 *}"
    assert len(u) == 3
    assert u.multiplier == Duration(2, 3)
    assert u.preprolated_duration == Duration(1, 4)
    assert u.prolated_duration == Duration(1, 4)


def test_Tuplet_02():
    '''Init empty fmtuplet.'''

    u = Tuplet(Fraction(2, 3), [])
    assert repr(u) == 'Tuplet(2/3, [])'
    assert str(u) == '{* 2/3 *}'
    assert len(u) == 0
    assert u.preprolated_duration == 0
    assert u.multiplier == Duration(2, 3)
    assert u.prolated_duration == 0


def test_Tuplet_03():
    '''Nest fmtuplet.'''

    u = Tuplet(Fraction(2, 3), [
        Tuplet(Fraction(4, 5), Note(0, (1, 16)) * 5),
        Note("c'4"),
        Note("c'4")])
    assert repr(u) == "Tuplet(2/3, [{* 5:4 c'16, c'16, c'16, c'16, c'16 *}, c'4, c'4])"
    assert str(u) == "{* 3:2 {* 5:4 c'16, c'16, c'16, c'16, c'16 *}, c'4, c'4 *}"
    assert len(u) == 3
    assert u.preprolated_duration == Duration(1, 2)
    assert u.multiplier == Duration(2, 3)
    assert u.prolated_duration == Duration(1, 2)
    assert repr(u[0]) == "Tuplet(4/5, [c'16, c'16, c'16, c'16, c'16])"
    assert str(u[0]) == "{* 5:4 c'16, c'16, c'16, c'16, c'16 *}"
    assert len(u[0]) == 5
    assert u[0].preprolated_duration == Duration(1, 4)
    assert u[0].multiplier == Duration(4, 5)
    assert u[0].prolated_duration == Duration(1, 6)


def test_Tuplet_04():
    '''Nest empty fmtuplet.'''

    u = Tuplet(Fraction(2, 3), [
        Tuplet(Fraction(4, 5), []),
        Note("c'4"),
        Note("c'4")])
    assert repr(u) == "Tuplet(2/3, [{* 4/5 *}, c'4, c'4])"
    assert str(u) == "{* 3:2 {* 4/5 *}, c'4, c'4 *}"
    assert len(u) == 3
    assert u.preprolated_duration == Duration(1, 3)
    assert u.multiplier == Duration(2, 3)
    assert u.prolated_duration == Duration(1, 3)
    assert repr(u[0]) == 'Tuplet(4/5, [])'
    assert str(u[0]) == '{* 4/5 *}'
    assert len(u[0]) == 0
    assert u[0].preprolated_duration == Duration(0)
    assert u[0].multiplier == Duration(4, 5)
    assert u[0].prolated_duration == Duration(0)
