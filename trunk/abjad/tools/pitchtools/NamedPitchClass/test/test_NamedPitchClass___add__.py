# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitchClass___add___01():

    npc = pitchtools.NamedPitchClass('c')

    new = npc + pitchtools.NamedMelodicInterval('perfect', 1)
    new == pitchtools.NamedPitchClass('c')

    new = npc + pitchtools.NamedMelodicInterval('minor', 2)
    new == pitchtools.NamedPitchClass('df')

    new = npc + pitchtools.NamedMelodicInterval('minor', -2)
    new == pitchtools.NamedPitchClass('b')

    new = npc + pitchtools.NamedMelodicInterval('major', 2)
    new == pitchtools.NamedPitchClass('d')

    new = npc + pitchtools.NamedMelodicInterval('major', -2)
    new == pitchtools.NamedPitchClass('bf')
