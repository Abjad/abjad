# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitchClassSet___hash___01():
    r'''Named pitch-class sets are hashable.
    '''

    npc_set = pitchtools.NamedPitchClassSet([
        pitchtools.NamedPitchClass('c'),
        pitchtools.NamedPitchClass('d'),
        pitchtools.NamedPitchClass('e'),])

    assert hash(npc_set) == hash(repr(npc_set))
