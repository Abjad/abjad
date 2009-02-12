from abjad.helpers.diatonic_to_chromatic import diatonic_to_chromatic

def test_diatonic_to_chromatic_01( ):
   assert diatonic_to_chromatic(0) == 0
   assert diatonic_to_chromatic(1) == 2
   assert diatonic_to_chromatic(2) == 4
   assert diatonic_to_chromatic(3) == 5
   assert diatonic_to_chromatic(4) == 7
   assert diatonic_to_chromatic(5) == 9
   assert diatonic_to_chromatic(6) == 11
   assert diatonic_to_chromatic(7) == 12
   assert diatonic_to_chromatic(8) == 14

   assert diatonic_to_chromatic(-1) == -1
   assert diatonic_to_chromatic(-2) == -3
   assert diatonic_to_chromatic(-3) == -5
   assert diatonic_to_chromatic(-4) == -7
   assert diatonic_to_chromatic(-5) == -8
   assert diatonic_to_chromatic(-6) == -10
   assert diatonic_to_chromatic(-7) == -12
   assert diatonic_to_chromatic(-8) == -13

