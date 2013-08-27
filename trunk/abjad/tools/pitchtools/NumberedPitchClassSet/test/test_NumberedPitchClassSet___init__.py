# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSet___init___01():
    r'''Works with numbers.
    '''

    assert len(pitchtools.NumberedPitchClassSet([0, 2, 6, 7])) == 4


def test_NumberedPitchClassSet___init___02():
    r'''Works with pitch-classes.
    '''

    assert len(pitchtools.NumberedPitchClassSet(
        [pitchtools.NumberedPitchClass(x) for x in [0, 2, 6, 7]])) == 4


def test_NumberedPitchClassSet___init___03():
    r'''Works with chords.
    '''

    chord = Chord([13, 14, 15], (1, 4))
    pitch_class_set = pitchtools.NumberedPitchClassSet(chord)
    assert len(pitch_class_set) == 3


def test_NumberedPitchClassSet___init___04():
    r'''Works with notes.
    '''

    note = Note(13, (1, 4))
    pitch_class_set = pitchtools.NumberedPitchClassSet([note])
    assert len(pitch_class_set) == 1
