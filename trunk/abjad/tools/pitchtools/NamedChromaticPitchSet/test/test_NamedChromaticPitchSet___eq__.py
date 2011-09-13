from abjad import *


def test_NamedChromaticPitchSet___eq___01():
    '''Pitch set equality works as expected.'''

    pset1 = pitchtools.NamedChromaticPitchSet([12, 14, 18, 19])
    pset2 = pitchtools.NamedChromaticPitchSet([12, 14, 18, 19])
    pset3 = pitchtools.NamedChromaticPitchSet([12, 14, 18, 20])

    assert pset1 == pset2
    assert pset1 != pset3
    assert pset2 != pset3
    assert not pset1 != pset2
