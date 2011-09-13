from abjad import *


def test_NumberedChromaticPitchClassSet___contains___01():
    '''PitchClassSet containment works as expected.'''

    pcset = pitchtools.NumberedChromaticPitchClassSet([0, 2, 6, 7])
    pc1 = pitchtools.NumberedChromaticPitchClass(2)
    pc2 = pitchtools.NumberedChromaticPitchClass(3)

    assert pc1 in pcset
    assert pc2 not in pcset
