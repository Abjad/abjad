from abjad import *


def test_NamedDiatonicPitch___init____01( ):

   assert isinstance(pitchtools.NamedDiatonicPitch("c''"), pitchtools.NamedDiatonicPitch)
