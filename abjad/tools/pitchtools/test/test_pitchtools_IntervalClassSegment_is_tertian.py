# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_IntervalClassSegment_is_tertian_01():

    dicseg = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('major', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('diminished', 3)])

    assert dicseg.is_tertian


def test_pitchtools_IntervalClassSegment_is_tertian_02():

    dicseg = pitchtools.IntervalClassSegment([
        pitchtools.NamedInversionEquivalentIntervalClass('major', 2),
        pitchtools.NamedInversionEquivalentIntervalClass('minor', 3),
        pitchtools.NamedInversionEquivalentIntervalClass('diminished', 3)])

    assert not dicseg.is_tertian
