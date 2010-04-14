from abjad import *


def test_NumericPitch_apply_accidental_01( ):

   assert pitchtools.NumericPitch(12).apply_accidental('sharp').number == 13
   assert pitchtools.NumericPitch(12).apply_accidental('flat').number == 11
   assert pitchtools.NumericPitch(12).apply_accidental('natural').number == 12


def test_NumericPitch_apply_accidental_02( ):

   assert pitchtools.NumericPitch(12).apply_accidental('quarter sharp').number \
      == 12.5
   assert pitchtools.NumericPitch(12).apply_accidental('quarter flat').number \
      == 11.5
