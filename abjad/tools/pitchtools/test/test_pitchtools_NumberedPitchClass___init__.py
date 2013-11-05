# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_pitchtools_NumberedPitchClass___init___01():
    r'''Pitch class initialization works with numbers.
    '''

    assert isinstance(pitchtools.NumberedPitchClass(0),
        pitchtools.NumberedPitchClass)
    assert isinstance(pitchtools.NumberedPitchClass(0.5),
        pitchtools.NumberedPitchClass)
    assert isinstance(pitchtools.NumberedPitchClass(1),
        pitchtools.NumberedPitchClass)
    assert isinstance(pitchtools.NumberedPitchClass(1.5),
        pitchtools.NumberedPitchClass)
    assert isinstance(pitchtools.NumberedPitchClass(13),
        pitchtools.NumberedPitchClass)
    assert isinstance(pitchtools.NumberedPitchClass(13.5),
        pitchtools.NumberedPitchClass)


def test_pitchtools_NumberedPitchClass___init___02():
    r'''Pitch class initialization works with other pitch-classes.
    '''

    pc = pitchtools.NumberedPitchClass(pitchtools.NumberedPitchClass(0))
    assert isinstance(pc, pitchtools.NumberedPitchClass)

    pc = pitchtools.NumberedPitchClass(pitchtools.NumberedPitchClass(12))
    assert isinstance(pc, pitchtools.NumberedPitchClass)


def test_pitchtools_NumberedPitchClass___init___03():
    r'''PitchClass initialization works with pitches.
    '''

    pc = pitchtools.NumberedPitchClass(pitchtools.NamedPitch(0))
    assert isinstance(pc, pitchtools.NumberedPitchClass)

    pc = pitchtools.NumberedPitchClass(pitchtools.NamedPitch(12))
    assert isinstance(pc, pitchtools.NumberedPitchClass)


def test_pitchtools_NumberedPitchClass___init___04():
    r'''Pitch class initialization works with notes.
    '''

    note = Note(13, (1, 4))
    pc = pitchtools.NumberedPitchClass(note)
    assert pc == pitchtools.NumberedPitchClass(1)


def test_pitchtools_NumberedPitchClass___init___05():
    r'''Pitch class initialization works with one-note chords.
    '''

    chord = Chord([13], (1, 4))
    pc = pitchtools.NumberedPitchClass(chord)
    assert pc == pitchtools.NumberedPitchClass(1)


def test_pitchtools_NumberedPitchClass___init___06():
    r'''Init with named pitch-class instance.
    '''

    npc = pitchtools.NamedPitchClass('cs')
    pc = pitchtools.NumberedPitchClass(npc)
    assert pc == pitchtools.NumberedPitchClass(1)


def test_pitchtools_NumberedPitchClass___init___07():
    r'''PitchClass initialization raises ValueError.
    '''

    assert py.test.raises(Exception, "pitchtools.NumberedPitchClass('foo')")


def test_pitchtools_NumberedPitchClass___init___08():
    r'''PitchClass initialization raises TypeError on rest.
    '''

    rest = Rest((1, 4))
    assert py.test.raises(Exception, 'pitchtools.NumberedPitchClass(rest)')


def test_pitchtools_NumberedPitchClass___init___09():
    r'''PitchClass initialization raises MissingPitchError on empty chord.
    '''

    chord = Chord([], (1, 4))
    assert py.test.raises(MissingPitchError, 'pitchtools.NumberedPitchClass(chord)')


def test_pitchtools_NumberedPitchClass___init___10():
    r'''Init from named pitch-class string.
    '''

    assert pitchtools.NumberedPitchClass('c') == 0
    assert pitchtools.NumberedPitchClass('cs') == 1
    assert pitchtools.NumberedPitchClass('cf') == 11
    assert pitchtools.NumberedPitchClass('css') == 2
