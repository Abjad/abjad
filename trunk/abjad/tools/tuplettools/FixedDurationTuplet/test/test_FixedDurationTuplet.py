from abjad import *


def test_FixedDurationTuplet_01():
    '''Nest typical fdtuplet.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3),
        Note(0, (1, 8)),
        Note(0, (1, 8)),
        Note(0, (1, 8))])
    assert repr(t) == "FixedDurationTuplet(1/2, [{@ 3:2 c'8, c'8, c'8 @}, c'8, c'8, c'8])"
    assert str(t) == "{@ 5:4 {@ 3:2 c'8, c'8, c'8 @}, c'8, c'8, c'8 @}"
    assert t.target_duration == Fraction(1, 2)
    assert t.multiplier == Fraction(4, 5)
    assert t.prolated_duration == Fraction(1, 2)
    assert repr(t[0]) == "FixedDurationTuplet(1/4, [c'8, c'8, c'8])"
    assert str(t[0]) == "{@ 3:2 c'8, c'8, c'8 @}"
    assert len(t[0]) == 3
    assert t[0].target_duration == Fraction(1, 4)
    assert t[0].multiplier == Fraction(2, 3)
    assert t[0].prolated_duration == Fraction(1, 5)


def test_FixedDurationTuplet_02():
    '''Nest empty fdtuplet.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 4), [
        tuplettools.FixedDurationTuplet(Duration(2, 8), []),
        Note(0, (1, 8)),
        Note(0, (1, 8)),
        Note(0, (1, 8))])
    assert repr(t) == "FixedDurationTuplet(1/2, [{@ 1/4 @}, c'8, c'8, c'8])"
    assert str(t) == "{@ 5:4 {@ 1/4 @}, c'8, c'8, c'8 @}"
    assert t.target_duration == Fraction(1, 2)
    assert t.multiplier == Fraction(4, 5)
    assert t.prolated_duration == Fraction(1, 2)
    assert repr(t[0]) == 'FixedDurationTuplet(1/4, [])'
    assert str(t[0]) == '{@ 1/4 @}'
    assert len(t[0]) == 0
    assert t[0].target_duration == Fraction(1, 4)
    assert t[0].multiplier == None
    assert t[0].prolated_duration == Fraction(1, 5)


def test_FixedDurationTuplet_03():
    '''Test 1-multiplier fdtuplet.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 2)
    assert repr(t) == "FixedDurationTuplet(1/4, [c'8, c'8])"
    assert str(t) == "{@ 1:1 c'8, c'8 @}"
    assert t.format == "{\n\tc'8\n\tc'8\n}"


def test_FixedDurationTuplet_04():
    '''Test 1-multiplier fdtuplet.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), Note(0, (1, 8)) * 3)
    t.pop()
    assert repr(t) == "FixedDurationTuplet(1/4, [c'8, c'8])"
    assert str(t) == "{@ 1:1 c'8, c'8 @}"
    assert t.format == "{\n\tc'8\n\tc'8\n}"


def test_FixedDurationTuplet_05():
    '''Tuplet.is_invisible formats compressed music.'''

    t = tuplettools.FixedDurationTuplet(Duration(1, 4), Note(0, (1, 8)) * 3)
    assert t.is_invisible is None
    t.is_invisible = True
    assert t.format == "\\scaleDurations #'(2 . 3) {\n\tc'8\n\tc'8\n\tc'8\n}"

    r'''
    \scaleDurations #'(2 . 3) {
        c'8
        c'8
        c'8
    }
    '''

    t.is_invisible = False
    assert t.format == "\\times 2/3 {\n\tc'8\n\tc'8\n\tc'8\n}"
