# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSet___eq___01():
    r'''PCset equality works as expected.
    '''

    pcset1 = pitchtools.NumberedPitchClassSet([0, 2, 6, 7])
    pcset2 = pitchtools.NumberedPitchClassSet([0, 2, 6, 7])
    pcset3 = pitchtools.NumberedPitchClassSet([0, 2, 6, 8])

    assert pcset1 == pcset2
    assert pcset1 != pcset3
    assert pcset2 != pcset3
    assert not pcset1 != pcset2
