from abjad import *


def test__Leaf_symmetric_difference_01():
    '''Chords completely disjunct; all pitches preserved.'''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([3, 4, 5], (1, 4))
    v = t ^ u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2, 3, 4, 5)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_symmetric_difference_02():
    '''Partially intersecting chords; shared pitches do not appear at all.'''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([1, 2, 3], (1, 4))
    v = t ^ u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 3)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_symmetric_difference_03():
    '''Wholly intersecting chords; returns no pitches at all.'''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([0, 1, 2], (1, 4))
    v = t ^ u
    assert isinstance(v, Rest)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_symmetric_difference_04():
    '''Enharmonically disjunct; enharmonic equivalents both appear.'''
    t = Chord([0, ('cs', 4), 2], (1, 4))
    u = Chord([0, ('df', 4), 2], (1, 4))
    v = t ^ u
    assert isinstance(v, Chord)
    assert v.written_pitches == (1, "df'")
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_symmetric_difference_05():
    '''Duration inequality; noncommutative operation takes duration from LHS.'''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([3, 4, 5], (1, 8))
    v = t ^ u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2, 3, 4, 5)
    assert v.written_duration == t.written_duration
    assert t is not u is not v


def test__Leaf_symmetric_difference_06():
    '''Duration inequality; noncommutative operation takes duration from LHS.'''
    t = Chord([0, 1, 2], (1, 8))
    u = Chord([3, 4, 5], (1, 4))
    v = t ^ u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2, 3, 4, 5)
    assert v.written_duration == t.written_duration
    assert t is not u is not v


def test__Leaf_symmetric_difference_07():
    '''Rest in symmetric difference with rest produces rest.'''
    t = Rest((1, 4))
    u = Rest((1, 4))
    v = t ^ u
    assert isinstance(v, Rest)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_symmetric_difference_08():
    '''Rest in symmetric difference with note produces note.'''
    t = Rest((1, 4))
    u = Note("c'4")
    v = t ^ u
    assert isinstance(v, Note)
    assert v.written_pitch == 0
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_symmetric_difference_09():
    '''Note in symmetric difference with like pitched note produces rest.'''
    t = Note("c'4")
    u = Note("c'4")
    v = t ^ u
    assert isinstance(v, Rest)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_symmetric_difference_10():
    '''Note in symmetric difference with differently pitched note produces chord.'''
    t = Note("c'4")
    u = Note(2, (1, 4))
    v = t ^ u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 2)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_symmetric_difference_11():
    '''Chord in symmetric difference with differently pitched note produces chord.'''
    t = Chord([0, 2], (1, 4))
    u = Note(4, (1, 4))
    v = t ^ u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 2, 4)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_symmetric_difference_12():
    '''Chord in symmetric difference with like pitched note removes shared note.'''
    t = Chord([0, 2], (1, 4))
    u = Note("c'4")
    v = t ^ u
    assert isinstance(v, Note)
    assert v.written_pitch == 2
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v
