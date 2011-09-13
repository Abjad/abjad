from abjad import *
from abjad.tools.pitchtools import NumberedDiatonicPitch


def test_NumberedDiatonicPitch___repr___01():
    '''Numbered diatonic pitch repr is evaluable.
    '''

    numbered_diatonic_pitch_1 = pitchtools.NumberedDiatonicPitch(0)
    numbered_diatonic_pitch_2 = eval(repr(numbered_diatonic_pitch_1))

    assert isinstance(numbered_diatonic_pitch_1, pitchtools.NumberedDiatonicPitch)
    assert isinstance(numbered_diatonic_pitch_2, pitchtools.NumberedDiatonicPitch)
