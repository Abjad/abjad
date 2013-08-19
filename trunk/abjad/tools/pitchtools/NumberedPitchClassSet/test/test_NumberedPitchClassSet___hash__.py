# -*- encoding: utf-8 -*-
from abjad import *


def test_NumberedPitchClassSet___hash___01():
    r'''Pitch class sets are hashable.
    '''

    pcset = pitchtools.NumberedPitchClassSet([0, 1, 2])

    assert hash(pcset) == hash(repr(pcset))
