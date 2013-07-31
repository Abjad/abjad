from abjad import *


def test_NamedChromaticPitchClassSet___hash___01():
    r'''Named pitch-class sets are hashable.
    '''

    npc_set = pitchtools.NamedChromaticPitchClassSet([
        pitchtools.NamedChromaticPitchClass('c'),
        pitchtools.NamedChromaticPitchClass('d'),
        pitchtools.NamedChromaticPitchClass('e'),])

    assert hash(npc_set) == hash(repr(npc_set))
