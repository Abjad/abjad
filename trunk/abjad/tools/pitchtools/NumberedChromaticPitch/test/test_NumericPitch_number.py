from abjad import *


def test_NumericPitch_number_01( ):

   assert pitchtools.NumberedChromaticPitch(12).number == 12
