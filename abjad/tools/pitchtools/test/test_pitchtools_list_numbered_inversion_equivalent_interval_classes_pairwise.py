# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_list_numbered_inversion_equivalent_interval_classes_pairwise_01():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

    iecics = pitchtools.list_numbered_inversion_equivalent_interval_classes_pairwise(
        staff[:],
        wrap=False,
        )

    assert iecics == [
        pitchtools.NumberedInversionEquivalentIntervalClass(2),
        pitchtools.NumberedInversionEquivalentIntervalClass(2), 
        pitchtools.NumberedInversionEquivalentIntervalClass(1), 
        pitchtools.NumberedInversionEquivalentIntervalClass(2), 
        pitchtools.NumberedInversionEquivalentIntervalClass(2), 
        pitchtools.NumberedInversionEquivalentIntervalClass(2), 
        pitchtools.NumberedInversionEquivalentIntervalClass(1),
        ]


def test_pitchtools_list_numbered_inversion_equivalent_interval_classes_pairwise_02():

    staff = Staff("c'8 d'8 e'8 f'8 g'8 a'8 b'8 c''8")

    iecics = pitchtools.list_numbered_inversion_equivalent_interval_classes_pairwise(
        staff[:],
        wrap=True,
        )

    assert iecics == [
        pitchtools.NumberedInversionEquivalentIntervalClass(2),
        pitchtools.NumberedInversionEquivalentIntervalClass(2), 
        pitchtools.NumberedInversionEquivalentIntervalClass(1), 
        pitchtools.NumberedInversionEquivalentIntervalClass(2), 
        pitchtools.NumberedInversionEquivalentIntervalClass(2), 
        pitchtools.NumberedInversionEquivalentIntervalClass(2), 
        pitchtools.NumberedInversionEquivalentIntervalClass(1), 
        pitchtools.NumberedInversionEquivalentIntervalClass(0),
        ]
