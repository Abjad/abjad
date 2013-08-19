# -*- encoding: utf-8 -*-
from abjad import *
import py.test


def test_NumberedChromaticPitchClass___init___01():
    r'''Pitch class initialization works with numbers.
    '''

    assert isinstance(pitchtools.NumberedChromaticPitchClass(0),
        pitchtools.NumberedChromaticPitchClass)
    assert isinstance(pitchtools.NumberedChromaticPitchClass(0.5),
        pitchtools.NumberedChromaticPitchClass)
    assert isinstance(pitchtools.NumberedChromaticPitchClass(1),
        pitchtools.NumberedChromaticPitchClass)
    assert isinstance(pitchtools.NumberedChromaticPitchClass(1.5),
        pitchtools.NumberedChromaticPitchClass)
    assert isinstance(pitchtools.NumberedChromaticPitchClass(13),
        pitchtools.NumberedChromaticPitchClass)
    assert isinstance(pitchtools.NumberedChromaticPitchClass(13.5),
        pitchtools.NumberedChromaticPitchClass)


def test_NumberedChromaticPitchClass___init___02():
    r'''Pitch class initialization works with other pitch-classes.
    '''

    pc = pitchtools.NumberedChromaticPitchClass(pitchtools.NumberedChromaticPitchClass(0))
    assert isinstance(pc, pitchtools.NumberedChromaticPitchClass)

    pc = pitchtools.NumberedChromaticPitchClass(pitchtools.NumberedChromaticPitchClass(12))
    assert isinstance(pc, pitchtools.NumberedChromaticPitchClass)


def test_NumberedChromaticPitchClass___init___03():
    r'''PitchClass initialization works with pitches.
    '''

    pc = pitchtools.NumberedChromaticPitchClass(pitchtools.NamedPitch(0))
    assert isinstance(pc, pitchtools.NumberedChromaticPitchClass)

    pc = pitchtools.NumberedChromaticPitchClass(pitchtools.NamedPitch(12))
    assert isinstance(pc, pitchtools.NumberedChromaticPitchClass)


def test_NumberedChromaticPitchClass___init___04():
    r'''Pitch class initialization works with notes.
    '''

    note = Note(13, (1, 4))
    pc = pitchtools.NumberedChromaticPitchClass(note)
    assert pc == pitchtools.NumberedChromaticPitchClass(1)


def test_NumberedChromaticPitchClass___init___05():
    r'''Pitch class initialization works with one-note chords.
    '''

    chord = Chord([13], (1, 4))
    pc = pitchtools.NumberedChromaticPitchClass(chord)
    assert pc == pitchtools.NumberedChromaticPitchClass(1)


def test_NumberedChromaticPitchClass___init___06():
    r'''Init with named pitch-class instance.
    '''

    npc = pitchtools.NamedPitchClass('cs')
    pc = pitchtools.NumberedChromaticPitchClass(npc)
    assert pc == pitchtools.NumberedChromaticPitchClass(1)


def test_NumberedChromaticPitchClass___init___07():
    r'''PitchClass initialization raises ValueError.
    '''

    assert py.test.raises(Exception, "pitchtools.NumberedChromaticPitchClass('foo')")


def test_NumberedChromaticPitchClass___init___08():
    r'''PitchClass initialization raises TypeError on rest.
    '''

    rest = Rest((1, 4))
    assert py.test.raises(Exception, 'pitchtools.NumberedChromaticPitchClass(rest)')


def test_NumberedChromaticPitchClass___init___09():
    r'''PitchClass initialization raises MissingPitchError on empty chord.
    '''

    chord = Chord([], (1, 4))
    assert py.test.raises(MissingPitchError, 'pitchtools.NumberedChromaticPitchClass(chord)')


def test_NumberedChromaticPitchClass___init___10():
    r'''Init from named pitch-class string.
    '''

    assert pitchtools.NumberedChromaticPitchClass('c') == 0
    assert pitchtools.NumberedChromaticPitchClass('cs') == 1
    assert pitchtools.NumberedChromaticPitchClass('cf') == 11
    assert pitchtools.NumberedChromaticPitchClass('css') == 2
