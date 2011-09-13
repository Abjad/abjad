from abjad import *


def test_NamedChromaticPitchClassSegment_inversion_equivalent_diatonic_interval_class_segment_01():

    npcseg = pitchtools.NamedChromaticPitchClassSegment(['c', 'd', 'e', 'f'])
    dicseg = pitchtools.InversionEquivalentDiatonicIntervalClassSegment([
        pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2),
        pitchtools.InversionEquivalentDiatonicIntervalClass('major', 2),
        pitchtools.InversionEquivalentDiatonicIntervalClass('minor', 2)])
    npcseg.inversion_equivalent_diatonic_interval_class_segment == dicseg
