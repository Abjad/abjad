# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedInversionEquivalentIntervalClass__init_by_quality_string_and_number_01():
    r'''Initializeunison.
    '''

    assert str(pitchtools.NamedInversionEquivalentIntervalClass('perfect', 1)) == 'P1'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('perfect', -1)) == 'P1'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('augmented', 1)) == 'aug1'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('augmented', -1)) == 'aug1'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('diminished', 1)) == 'dim1'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('diminished', -1)) == 'dim1'


def test_pitchtools_NamedInversionEquivalentIntervalClass__init_by_quality_string_and_number_02():
    r'''Initialize usual cases.
    '''

    assert str(pitchtools.NamedInversionEquivalentIntervalClass('minor', 2)) == '+m2'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('major', 2)) == '+M2'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('minor', 3)) == '+m3'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('major', 3)) == '+M3'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('perfect', 4)) == '+P4'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('augmented', 4)) == '+aug4'


def test_pitchtools_NamedInversionEquivalentIntervalClass__init_by_quality_string_and_number_03():
    r'''Initialize inverted cases less than one octave.
    '''

    assert str(pitchtools.NamedInversionEquivalentIntervalClass('major', 7)) == '+m2'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('minor', 7)) == '+M2'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('major', 6)) == '+m3'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('minor', 6)) == '+M3'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('perfect', 5)) == '+P4'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('diminished', 5)) == '+aug4'


def test_pitchtools_NamedInversionEquivalentIntervalClass__init_by_quality_string_and_number_04():
    r'''Initialize noninverted cases greater than one octave.
    '''

    assert str(pitchtools.NamedInversionEquivalentIntervalClass('minor', 9)) == '+m2'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('major', 9)) == '+M2'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('minor', 10)) == '+m3'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('major', 10)) == '+M3'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('perfect', 11)) == '+P4'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('augmented', 11)) == '+aug4'


def test_pitchtools_NamedInversionEquivalentIntervalClass__init_by_quality_string_and_number_05():
    r'''Initialize inverted cases greater than one octave.
    '''

    assert str(pitchtools.NamedInversionEquivalentIntervalClass('major', 14)) == '+m2'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('minor', 14)) == '+M2'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('major', 13)) == '+m3'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('minor', 13)) == '+M3'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('perfect', 12)) == '+P4'
    assert str(pitchtools.NamedInversionEquivalentIntervalClass('diminished', 12)) == '+aug4'
