from abjad import *
from abjad.tools.pitchtools import NamedDiatonicPitch


def test_NamedDiatonicPitch___repr___01():
    '''Named diatonic pitch repr is evaluable.
    '''

    named_diatonic_pitch_1 = pitchtools.NamedDiatonicPitch("c''")
    named_diatonic_pitch_2 = eval(repr(named_diatonic_pitch_1))

    '''NamedDiatonicPitch("c''")'''

    assert isinstance(named_diatonic_pitch_1, pitchtools.NamedDiatonicPitch)
    assert isinstance(named_diatonic_pitch_2, pitchtools.NamedDiatonicPitch)
