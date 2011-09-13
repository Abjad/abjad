from abjad import *
from abjad.tools.pitchtools import NumberedChromaticPitch


def test_NumberedChromaticPitch___repr___01():
    '''Numbered chromatic pitch repr is evaluable.
    '''

    numbered_chromatic_pitch_1 = pitchtools.NumberedChromaticPitch(13)
    numbered_chromatic_pitch_2 = eval(repr(numbered_chromatic_pitch_1))

    assert isinstance(numbered_chromatic_pitch_1, pitchtools.NumberedChromaticPitch)
    assert isinstance(numbered_chromatic_pitch_2, pitchtools.NumberedChromaticPitch)
