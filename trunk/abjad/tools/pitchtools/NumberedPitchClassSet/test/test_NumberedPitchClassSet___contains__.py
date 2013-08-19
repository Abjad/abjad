# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSet___contains___01():
    r'''PitchClassSet containment works as expected.
    '''

    pcset = pitchtools.NumberedPitchClassSet([0, 2, 6, 7])
    pc1 = pitchtools.NumberedPitchClass(2)
    pc2 = pitchtools.NumberedPitchClass(3)

    assert pc1 in pcset
    assert pc2 not in pcset
