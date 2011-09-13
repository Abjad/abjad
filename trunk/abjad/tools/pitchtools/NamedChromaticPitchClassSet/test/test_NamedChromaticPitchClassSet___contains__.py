from abjad import *


def test_NamedChromaticPitchClassSet___contains___01():
    '''NamedChromaticPitchClassSet containment works as expected.'''

    npc_set = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),])

    assert pitchtools.NamedChromaticPitchClass('c') in npc_set
    assert pitchtools.NamedChromaticPitchClass('d') in npc_set
    assert pitchtools.NamedChromaticPitchClass('e') in npc_set

    assert not pitchtools.NamedChromaticPitchClass('cs') in npc_set
    assert not pitchtools.NamedChromaticPitchClass('cf') in npc_set
