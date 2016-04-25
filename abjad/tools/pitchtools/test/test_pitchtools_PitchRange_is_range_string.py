# -*- coding: utf-8 -*-
from abjad import *


def test_pitchtools_PitchRange_is_range_string_01():

    assert pitchtools.PitchRange.is_range_string('[A#0, Cb~8]')
    assert pitchtools.PitchRange.is_range_string("(A#+0, cs'')")
    assert pitchtools.PitchRange.is_range_string('[c, a)')
    assert pitchtools.PitchRange.is_range_string('(b,,, ctqs]')


def test_pitchtools_PitchRange_is_range_string_02():

    assert not pitchtools.PitchRange.is_range_string('')
    assert not pitchtools.PitchRange.is_range_string('foo')
    assert not pitchtools.PitchRange.is_range_string(True)
    assert not pitchtools.PitchRange.is_range_string(7)
