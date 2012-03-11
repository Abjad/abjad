from abjad import *


def test__Leaf_set_minus_01():
    '''Chords completely disjunct; all RH pitches preserved.'''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([3, 4, 5], (1, 4))
    v = t - u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2)
    assert t is not u is not v


def test__Leaf_set_minus_02():
    '''Partially intersecting chords; shared pitches removed from RHS.'''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([1, 2, 3], (1, 4))
    v = t - u
    assert isinstance(v, Note)
    assert v.written_pitch == 0
    assert t is not u is not v


def test__Leaf_set_minus_03():
    '''Wholly intersecting chords; all pitches removed and rest returns.'''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([0, 1, 2], (1, 4))
    v = t - u
    assert isinstance(v, Rest)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_set_minus_04():
    '''Enharmonically disjunct; enharmonic RHS equivalent appears;
        shared pitches disappear.'''
    t = Chord([0, ('cs', 4), 2], (1, 4))
    u = Chord([0, ('df', 4), 2], (1, 4))
    v = t - u
    assert isinstance(v, Note)
    assert v.written_pitch == 1
    assert t is not u is not v


def test__Leaf_set_minus_05():
    '''Duration inequality; noncommutative operation takes duration from LHS.'''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([3, 4, 5], (1, 8))
    v = t - u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2)
    assert v.written_duration == t.written_duration
    assert t is not u is not v


def test__Leaf_set_minus_06():
    '''Duration inequality; noncommutative operation takes duration from LHS.'''
    t = Chord([0, 1, 2], (1, 8))
    u = Chord([3, 4, 5], (1, 4))
    v = t - u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2)
    assert v.written_duration == t.written_duration
    assert t is not u is not v


def test__Leaf_set_minus_07():
    '''Rest from from produces rest.'''
    t = Rest((1, 4))
    u = Rest((1, 4))
    v = t - u
    assert isinstance(v, Rest)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_set_minus_08():
    '''Note from rest produces rest.'''
    t = Rest((1, 4))
    u = Note("c'4")
    v = t - u
    assert isinstance(v, Rest)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_set_minus_09():
    '''Note from like pitched note produces rest.'''
    t = Note("c'4")
    u = Note("c'4")
    v = t - u
    assert isinstance(v, Rest)
    assert v.written_duration == Duration(1, 4)
    assert t is not u is not v


def test__Leaf_set_minus_10():
    '''Note from differently pitched note produces note.'''
    t = Note("c'4")
    u = Note(2, (1, 4))
    v = t - u
    assert isinstance(v, Note)
    assert v.written_pitch == 0
    assert t is not u is not v


def test__Leaf_set_minus_11():
    '''Differently pitched note from chord produces chord.'''
    t = Chord([0, 2], (1, 4))
    u = Note(4, (1, 4))
    v = t - u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 2)
    assert t is not u is not v


def test__Leaf_set_minus_12():
    '''Like pitched note from chord removes pitch.'''
    t = Chord([0, 2], (1, 4))
    u = Note("c'4")
    v = t - u
    assert isinstance(v, Note)
    assert v.written_pitch == 2
    assert t is not u is not v
