from abjad import *


def test_NamedChromaticPitchClassSet___eq___01():
    '''Named pitch-class set equality works as expected.'''

    npc_set_1 = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),])

    npc_set_2 = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),])

    npc_set_3 = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('e'),
        pitchtools.NamedChromaticPitchClass('f'),
        pitchtools.NamedChromaticPitchClass('g'),])

    assert npc_set_1 == npc_set_1
    assert npc_set_1 == npc_set_2
    assert npc_set_1 != npc_set_3
    assert npc_set_2 != npc_set_3
