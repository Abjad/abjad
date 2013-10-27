# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.markuptools import Markup
from abjad.tools.pitchtools import NamedPitch
from abjad.tools.pitchtools import PitchRange


def test_pitchtools_PitchRange___repr___01():
    r'''Pitch range reprs are evaluable.
    '''

    pitch_range_1 = pitchtools.PitchRange(-12, 36)
    pitch_range_2 = eval(repr(pitch_range_1))

    assert isinstance(pitch_range_1, PitchRange)
    assert isinstance(pitch_range_2, PitchRange)

    assert pitch_range_1 == pitch_range_2
    assert not pitch_range_1 is pitch_range_2


def test_pitchtools_PitchRange___repr___02():

    pitch_range = pitchtools.PitchRange(-12, 36, pitch_range_name='four-octave range')
    assert repr(pitch_range) == r'''PitchRange('[C3, C7]', pitch_range_name='four-octave range', pitch_range_name_markup=Markup(('four-octave range',)))'''


    pitch_range = pitchtools.PitchRange(-12, 36, pitch_range_name_markup=Markup('four-octave range'))
    assert repr(pitch_range) == r'''PitchRange('[C3, C7]', pitch_range_name_markup=Markup(('four-octave range',)))'''


#def test_pitchtools_PitchRange___repr___03():
#    r'''Repr works on empty pitch range.
#    '''
#
#    pitch_range == pitchtools.PitchRange()
#    assert repr(pitch_range) == "PitchRange('[]')"
