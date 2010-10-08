from abjad import *


def test_NumericPitch___neg___01( ):

   assert -pitchtools.NumberedChromaticPitch(12).number == -12
