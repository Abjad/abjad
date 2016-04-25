# -*- coding: utf-8 -*-
from abjad import *
import copy


def test_pitchtools_NamedPitchClass___copy___01():

    npc = pitchtools.NamedPitchClass('cs')
    new = copy.copy(npc)

    assert new == npc
    assert new is not npc
