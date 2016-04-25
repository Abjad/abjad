# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchClassSet___contains___01():
    r'''PitchClassSet containment works as expected.
    '''

    named_pitch_class_set = pitchtools.PitchClassSet([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),])

    assert pitchtools.NamedPitchClass('c') in named_pitch_class_set
    assert pitchtools.NamedPitchClass('d') in named_pitch_class_set
    assert pitchtools.NamedPitchClass('e') in named_pitch_class_set

    assert not pitchtools.NamedPitchClass('cs') in named_pitch_class_set
    assert not pitchtools.NamedPitchClass('cf') in named_pitch_class_set


def test_pitchtools_PitchClassSet___contains___02():
    r'''PitchClassSet containment works as expected.
    '''

    pitch_class_set = pitchtools.PitchClassSet([0, 2, 6, 7])
    pitch_class_1 = pitchtools.NumberedPitchClass(2)
    pitch_class_2 = pitchtools.NumberedPitchClass(3)

    assert pitch_class_1 in pitch_class_set
    assert pitch_class_2 not in pitch_class_set
