from abjad import *


def test_pitchtools_list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

    iecics = pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers(
        staff, wrap = False)

    assert iecics == [pitchtools.InversionEquivalentChromaticIntervalClass(2),
        pitchtools.InversionEquivalentChromaticIntervalClass(2), pitchtools.InversionEquivalentChromaticIntervalClass(1),         pitchtools.InversionEquivalentChromaticIntervalClass(2), pitchtools.InversionEquivalentChromaticIntervalClass(2),         pitchtools.InversionEquivalentChromaticIntervalClass(2), pitchtools.InversionEquivalentChromaticIntervalClass(1)]


def test_pitchtools_list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

    iecics = pitchtools.list_inversion_equivalent_chromatic_interval_classes_pairwise_between_pitch_carriers(
        staff, wrap = True)

    assert iecics == [pitchtools.InversionEquivalentChromaticIntervalClass(2),
        pitchtools.InversionEquivalentChromaticIntervalClass(2), pitchtools.InversionEquivalentChromaticIntervalClass(1),         pitchtools.InversionEquivalentChromaticIntervalClass(2), pitchtools.InversionEquivalentChromaticIntervalClass(2),         pitchtools.InversionEquivalentChromaticIntervalClass(2), pitchtools.InversionEquivalentChromaticIntervalClass(1),         pitchtools.InversionEquivalentChromaticIntervalClass(0)]
