from abjad import *


def test_NumberedChromaticPitch_semitones_01( ):

   assert pitchtools.NumberedChromaticPitch(12).semitones == 12
