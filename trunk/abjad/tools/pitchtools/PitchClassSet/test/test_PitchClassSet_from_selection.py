# -*- encoding: utf-8 -*-
from abjad import *


def test_PitchClassSet___init___02():
    r'''Works with chords.
    '''

    chord = Chord([12, 14, 16], (1, 4))
    named_pitch_class_set_1 = pitchtools.PitchClassSet.from_selection(chord)

    named_pitch_class_set_2 = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e')])

    assert named_pitch_class_set_1 == named_pitch_class_set_2


def test_PitchClassSet___init___03():
    r'''Works with notes.
    '''

    note = Note(13, (1, 4))
    named_pitch_class_set_1 = pitchtools.PitchClassSet.from_selection([note])

    named_pitch_class_set_2 = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('cs')])

    assert named_pitch_class_set_1 == named_pitch_class_set_2


def test_PitchClassSet___init___06():
    r'''Works with chords.
    '''

    chord = Chord([13, 14, 15], (1, 4))
    pitch_class_set = pitchtools.PitchClassSet.from_selection(chord)
    assert len(pitch_class_set) == 3


def test_PitchClassSet___init___07():
    r'''Works with notes.
    '''

    note = Note(13, (1, 4))
    pitch_class_set = pitchtools.PitchClassSet.from_selection([note])
    assert len(pitch_class_set) == 1
