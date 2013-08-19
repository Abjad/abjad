# -*- encoding: utf-8 -*-
from abjad import *
import copy


def test_NumberedInversionEquivalentIntervalClass___copy___01():

    ic1 = pitchtools.NumberedInversionEquivalentIntervalClass(1)
    new = copy.copy(ic1)

    assert ic1 == new
    assert not ic1 is new
