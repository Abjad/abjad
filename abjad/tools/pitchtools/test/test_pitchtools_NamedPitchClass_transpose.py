# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitchClass_transpose_01():

    npc = pitchtools.NamedPitchClass('c')

    new = npc.transpose(pitchtools.NamedInterval('perfect', 1))
    new == pitchtools.NamedPitchClass('c')

    new = npc.transpose(pitchtools.NamedInterval('minor', 2))
    new == pitchtools.NamedPitchClass('df')

    new = npc.transpose(pitchtools.NamedInterval('minor', -2))
    new == pitchtools.NamedPitchClass('b')

    new = npc.transpose(pitchtools.NamedInterval('major', 2))
    new == pitchtools.NamedPitchClass('d')

    new = npc.transpose(pitchtools.NamedInterval('major', -2))
    new == pitchtools.NamedPitchClass('bf')
