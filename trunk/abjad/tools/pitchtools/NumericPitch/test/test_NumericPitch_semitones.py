from abjad import *


def test_NumericPitch_semitones_01( ):

   assert pitchtools.NumericPitch(12).semitones == 12
