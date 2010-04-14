from abjad import *


def test_NumericPitch___neg___01( ):

   assert -pitchtools.NumericPitch(12).number == -12
