# -*- encoding: utf-8 -*-
from abjad import *


def test_NamedPitchClassSegment_inversion_equivalent_diatonic_interval_class_segment_01():

    npcseg = pitchtools.NamedPitchClassSegment(['c', 'd', 'e', 'f'])
    dicseg = pitchtools.NamedInversionEquivalentIntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('major', 2),
        pitchtools.NamedInversionEquivalentIntervalClass('major', 2),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 2)])
    npcseg.inversion_equivalent_diatonic_interval_class_segment == dicseg
