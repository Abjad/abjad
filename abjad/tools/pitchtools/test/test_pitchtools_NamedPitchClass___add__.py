# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitchClass___add___01():

    npc = pitchtools.NamedPitchClass('c')

    new = npc + pitchtools.NamedInterval('perfect', 1)
    new == pitchtools.NamedPitchClass('c')

    new = npc + pitchtools.NamedInterval('minor', 2)
    new == pitchtools.NamedPitchClass('df')

    new = npc + pitchtools.NamedInterval('minor', -2)
    new == pitchtools.NamedPitchClass('b')

    new = npc + pitchtools.NamedInterval('major', 2)
    new == pitchtools.NamedPitchClass('d')

    new = npc + pitchtools.NamedInterval('major', -2)
    new == pitchtools.NamedPitchClass('bf')
