from abjad import *


def test_measures_fuse_01( ):
   '''Fuse binary measures with different denominators.
      Helpers selects minimum of two denominators.
      Beams are OK because they attach to leaves rather than containers.'''

   t = Voice(measures_make([(1, 8), (2, 16)]))
   measures_populate(t, Rational(1, 16))
   diatonicize(t)
   Beam(t.leaves)

   r'''
   \new Voice {
         \time 1/8
         c'16 [
         d'16
         \time 2/16
         e'16
         f'16 ]
   }
   '''

   measures_fuse(t[0], t[1])

   r'''
   \new Voice {
         \time 2/8
         c'16 [
         d'16
         e'16
         f'16 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\t\\time 2/8\n\t\tc'16 [\n\t\td'16\n\t\te'16\n\t\tf'16 ]\n}"


 
def test_measures_fuse_02( ):
   '''Fuse binary measures with different denominators.
      Helpers selects minimum of two denominators.
      Beams are OK because they attach to leaves rather than containers.'''

   t = Voice(measures_make([(1, 8), (2, 16)]))
   measures_populate(t, Rational(1, 16))
   diatonicize(t)
   Beam(t[0])

   r'''
   \new Voice {
         \time 1/8
         c'16 [
         d'16 ]
         \time 2/16
         e'16
         f'16
   }
   '''

   measures_fuse(t[0], t[1])

   r'''
   \new Voice {
         \time 2/8
         c'16 [
         d'16
         e'16
         f'16 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\t\\time 2/8\n\t\tc'16 [\n\t\td'16\n\t\te'16\n\t\tf'16 ]\n}"
