from abjad import *


def test_PitchClass_apply_accidental_01( ):

   pc = pitchtools.PitchClass(11)

   assert pc.apply_accidental('sharp') == pitchtools.PitchClass(0)
   assert pc.apply_accidental('flat') == pitchtools.PitchClass(10)
   assert pc.apply_accidental('double sharp') == pitchtools.PitchClass(1)
   assert pc.apply_accidental('double flat') == pitchtools.PitchClass(9)
   assert pc.apply_accidental('quarter sharp') == pitchtools.PitchClass(11.5)
   assert pc.apply_accidental('quarter flat') == pitchtools.PitchClass(10.5)
