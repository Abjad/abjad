# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NumberedInversionEquivalentIntervalClass___eq___01():

    ic1 = pitchtools.NumberedInversionEquivalentIntervalClass(1)
    ic2 = pitchtools.NumberedInversionEquivalentIntervalClass(1)
    ic3 = pitchtools.NumberedInversionEquivalentIntervalClass(2)

    assert ic1 == ic2
    assert ic2 == ic1

    assert not ic2 == ic3
    assert not ic3 == ic2

    assert not ic3 == ic1
    assert not ic1 == ic3
