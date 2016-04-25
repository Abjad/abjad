# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_NamedPitchClass___sub___01():

    mdi = pitchtools.NamedPitchClass('c') - pitchtools.NamedPitchClass('d')
    assert mdi == pitchtools.NamedInversionEquivalentIntervalClass('major', 2)

    mdi = pitchtools.NamedPitchClass('d') - pitchtools.NamedPitchClass('c')
    assert mdi == pitchtools.NamedInversionEquivalentIntervalClass('major', 2)


def test_pitchtools_NamedPitchClass___sub___02():

    mdi = pitchtools.NamedPitchClass('c') - pitchtools.NamedPitchClass('cf')
    assert mdi == pitchtools.NamedInversionEquivalentIntervalClass('augmented', 1)

    mdi = pitchtools.NamedPitchClass('cf') - pitchtools.NamedPitchClass('c')
    assert mdi == pitchtools.NamedInversionEquivalentIntervalClass('augmented', 1)
