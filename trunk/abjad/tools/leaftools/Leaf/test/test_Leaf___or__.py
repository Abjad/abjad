# -*- encoding: utf-8 -*-
from abjad import *


def test_Leaf___or___01():
    r'''Chords completely disjunct; all pitches preserved.
    '''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([3, 4, 5], (1, 4))
    v = t | u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2, 3, 4, 5)
    assert t is not u is not v


def test_Leaf___or___02():
    r'''Partially intersecting chords; shared pitches appear only once.
    '''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([1, 2, 3], (1, 4))
    v = t | u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2, 3)
    assert t is not u is not v


def test_Leaf___or___03():
    r'''Wholly intersecting chords; shared pitches appear only once.
    '''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([0, 1, 2], (1, 4))
    v = t | u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2)
    assert t is not u is not v


def test_Leaf___or___04():
    r'''Enharmonically disjunct; enharmonic equivalents both appear.
    '''
    t = Chord([0, ('cs', 4), 2], (1, 4))
    u = Chord([0, ('df', 4), 2], (1, 4))
    v = t | u
    assert isinstance(v, Chord)
    assert v.written_pitches == ("c'", "cs'", "df'", "d'")
    assert t is not u is not v


def test_Leaf___or___05():
    r'''Differing durations; noncommutative union takes from LHS.
    '''
    t = Chord([0, 1, 2], (1, 4))
    u = Chord([3, 4, 5], (1, 8))
    v = t | u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 1, 2, 3, 4, 5)
    assert v.written_duration == t.written_duration
    assert t is not u is not v


def test_Leaf___or___06():
    r'''Differing durations; noncommutative union takes from LHS.
    '''
    t = Chord([0, 1, 2], (1, 8))
    u = Chord([3, 4, 5], (1, 4))
    v = t | u
    assert isinstance(v, Chord)
    assert v.written_duration == Duration(1, 8)
    assert t is not u is not v


def test_Leaf___or___07():
    r'''Rest in union with note produces note.
    '''
    t = Rest((1, 4))
    u = Note("c'4")
    v = t | u
    assert isinstance(v, Note)
    assert v.written_pitch == 0
    assert t is not u is not v


def test_Leaf___or___08():
    r'''Note in union with like pitched note produces note.
    '''
    t = Note("c'4")
    u = Note("c'4")
    v = t | u
    assert isinstance(v, Note)
    assert v.written_pitch == 0
    assert t is not u is not v


def test_Leaf___or___09():
    r'''Note in union with differently pitched note produces chord.
    '''
    t = Note("c'4")
    u = Note(2, (1, 4))
    v = t | u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 2)
    assert t is not u is not v


def test_Leaf___or___10():
    r'''Chord in union with differently pitched note produces chord.
    '''
    t = Chord([0, 2], (1, 4))
    u = Note(4, (1, 4))
    v = t | u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 2, 4)
    assert t is not u is not v


def test_Leaf___or___11():
    r'''Chord in union with like pitched note produces chord.
    '''
    t = Chord([0, 2], (1, 4))
    u = Note("c'4")
    v = t | u
    assert isinstance(v, Chord)
    assert v.written_pitches == (0, 2)
    assert t is not u is not v
