# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_pitchtools_NumberedPitchClass___init___01():
    r'''Pitch-class initialization works with numbers.
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

    pitch_class = pitchtools.NumberedPitchClass(pitchtools.NumberedPitchClass(0))
    assert isinstance(pitch_class, pitchtools.NumberedPitchClass)

    pitch_class = pitchtools.NumberedPitchClass(pitchtools.NumberedPitchClass(12))
    assert isinstance(pitch_class, pitchtools.NumberedPitchClass)


def test_pitchtools_NumberedPitchClass___init___03():
    r'''Pitch-class initialization works with pitches.
    '''

    pitch_class = pitchtools.NumberedPitchClass(NamedPitch(0))
    assert isinstance(pitch_class, pitchtools.NumberedPitchClass)

    pitch_class = pitchtools.NumberedPitchClass(NamedPitch(12))
    assert isinstance(pitch_class, pitchtools.NumberedPitchClass)


def test_pitchtools_NumberedPitchClass___init___04():
    r'''Pitch class initialization works with notes.
    '''

    note = Note(13, (1, 4))
    pitch_class = pitchtools.NumberedPitchClass(note)
    assert pitch_class == pitchtools.NumberedPitchClass(1)


def test_pitchtools_NumberedPitchClass___init___05():
    r'''Pitch class initialization works with one-note chords.
    '''

    chord = Chord([13], (1, 4))
    pitch_class = pitchtools.NumberedPitchClass(chord)
    assert pitch_class == pitchtools.NumberedPitchClass(1)


def test_pitchtools_NumberedPitchClass___init___06():
    r'''Initialize with named pitch-class instance.
    '''

    npc = pitchtools.NamedPitchClass('cs')
    pitch_class = pitchtools.NumberedPitchClass(npc)
    assert pitch_class == pitchtools.NumberedPitchClass(1)


def test_pitchtools_NumberedPitchClass___init___07():
    r'''Pitch-class initialization raises exception.
    '''

    assert pytest.raises(Exception, "pitchtools.NumberedPitchClass('foo')")


def test_pitchtools_NumberedPitchClass___init___08():
    r'''Pitch-class initialization raises TypeError on rest.
    '''

    rest = Rest((1, 4))
    assert pytest.raises(Exception, 'pitchtools.NumberedPitchClass(rest)')


def test_pitchtools_NumberedPitchClass___init___09():
    r'''Pitch-class initialization raises exception on empty chord.
    '''

    chord = Chord([], (1, 4))
    assert pytest.raises(Exception, 'pitchtools.NumberedPitchClass(chord)')


def test_pitchtools_NumberedPitchClass___init___10():
    r'''Initialize from named pitch-class string.
    '''

    assert pitchtools.NumberedPitchClass('c') == 0
    assert pitchtools.NumberedPitchClass('cs') == 1
    assert pitchtools.NumberedPitchClass('cf') == 11
    assert pitchtools.NumberedPitchClass('css') == 2
