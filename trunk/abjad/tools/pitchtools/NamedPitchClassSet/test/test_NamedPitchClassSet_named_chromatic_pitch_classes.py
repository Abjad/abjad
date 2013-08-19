# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitchClassSet_named_chromatic_pitch_classes_01():

    npc_set = pitchtools.NamedPitchClassSet([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),])
    pitch_classes = npc_set.named_chromatic_pitch_classes

    assert isinstance(pitch_classes, tuple)

    assert pitch_classes[0] == pitchtools.NamedPitchClass('c')
    assert pitch_classes[1] == pitchtools.NamedPitchClass('d')
    assert pitch_classes[2] == pitchtools.NamedPitchClass('e')
