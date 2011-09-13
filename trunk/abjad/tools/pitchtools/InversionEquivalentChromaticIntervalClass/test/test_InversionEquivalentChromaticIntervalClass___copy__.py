from abjad import *
import copy


def test_InversionEquivalentChromaticIntervalClass___copy___01():

    ic1 = pitchtools.InversionEquivalentChromaticIntervalClass(1)
    new = copy.copy(ic1)

    assert ic1 == new
    assert not ic1 is new
