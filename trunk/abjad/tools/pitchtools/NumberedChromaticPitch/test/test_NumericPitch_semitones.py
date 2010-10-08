from abjad import *


def test_NumericPitch_semitones_01( ):

   assert pitchtools.NumberedChromaticPitch(12).semitones == 12
