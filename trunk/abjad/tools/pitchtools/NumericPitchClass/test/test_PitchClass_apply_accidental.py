from abjad import *


def test_PitchClass_apply_accidental_01( ):

   pc = pitchtools.NumericPitchClass(11)

   assert pc.apply_accidental('sharp') == pitchtools.NumericPitchClass(0)
   assert pc.apply_accidental('flat') == pitchtools.NumericPitchClass(10)
   assert pc.apply_accidental('double sharp') == pitchtools.NumericPitchClass(1)
   assert pc.apply_accidental('double flat') == pitchtools.NumericPitchClass(9)
   assert pc.apply_accidental('quarter sharp') == pitchtools.NumericPitchClass(11.5)
   assert pc.apply_accidental('quarter flat') == pitchtools.NumericPitchClass(10.5)
