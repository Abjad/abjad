from abjad import *
from abjad.tools.markuptools import Markup


def test_pitchtools_PitchRange_pitch_range_name_markup_01():

    pitch_range = pitchtools.PitchRange(-12, 36)
    assert pitch_range.pitch_range_name_markup is None


def test_pitchtools_PitchRange_pitch_range_name_markup_02():

    pitch_range = pitchtools.PitchRange(-12, 36, pitch_range_name='four-octave range')
    assert pitch_range.pitch_range_name_markup == Markup('four-octave range')


def test_pitchtools_PitchRange_pitch_range_name_markup_03():

    pitch_range = pitchtools.PitchRange(-12, 36, pitch_range_name_markup=Markup('four-octave range'))
    assert pitch_range.pitch_range_name_markup == Markup('four-octave range')


def test_pitchtools_PitchRange_pitch_range_name_markup_04():

    pitch_range = pitchtools.PitchRange(-12, 36, 
        pitch_range_name='foo', pitch_range_name_markup=Markup('four-octave range'))
    assert pitch_range.pitch_range_name == 'foo'
    assert pitch_range.pitch_range_name_markup == Markup('four-octave range')
