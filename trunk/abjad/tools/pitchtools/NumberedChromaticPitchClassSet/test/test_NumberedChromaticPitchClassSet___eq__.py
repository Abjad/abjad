from abjad import *


def test_NumberedChromaticPitchClassSet___eq___01():
    '''PCset equality works as expected.'''

    pcset1 = pitchtools.NumberedChromaticPitchClassSet([0, 2, 6, 7])
    pcset2 = pitchtools.NumberedChromaticPitchClassSet([0, 2, 6, 7])
    pcset3 = pitchtools.NumberedChromaticPitchClassSet([0, 2, 6, 8])

    assert pcset1 == pcset2
    assert pcset1 != pcset3
    assert pcset2 != pcset3
    assert not pcset1 != pcset2
