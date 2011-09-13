from abjad import *


def test_InversionEquivalentDiatonicIntervalClassSegment_is_tertian_01():

    dicseg = pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
        pitchtools.InversionEquivalentDiatonicIntervalClass('major', 3),
        pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
        pitchtools.InversionEquivalentDiatonicIntervalClass('diminshed', 3)])

    assert dicseg.is_tertian


def test_InversionEquivalentDiatonicIntervalClassSegment_is_tertian_02():

    dicseg = pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
        pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2),
        pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 3),
        pitchtools.InversionEquivalentDiatonicIntervalClass('diminshed', 3)])

    assert not dicseg.is_tertian
