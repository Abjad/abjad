from abjad import *


### TODO: write tests with tuplets inside measures

def test_measures_decompose_01( ):
   '''Decompose binary measures in voice.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 2)
   diatonicize(t)
   Beam(t[:])

   r'''
   \new Voice {
         \time 2/8
         c'8 [
         d'8
         \time 2/8
         e'8
         f'8 ]
   }
   '''

   measures_decompose(t)

   r'''
   \new Voice {
         \time 1/8
         c'8 [
         \time 1/8
         d'8
         \time 1/8
         e'8
         \time 1/8
         f'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\t\\time 1/8\n\t\tc'8 [\n\t\t\\time 1/8\n\t\td'8\n\t\t\\time 1/8\n\t\te'8\n\t\t\\time 1/8\n\t\tf'8 ]\n}"


def test_measures_decompose_02( ):
   '''Decompose nonbinary measures in voice.'''

   t = Voice(RigidMeasure((2, 12), run(2)) * 2)
   diatonicize(t)
   Beam(t[:])

   r'''
   \new Voice {
         \time 2/12
         \scaleDurations #'(2 . 3) {
            c'8 [
            d'8
         }
         \time 2/12
         \scaleDurations #'(2 . 3) {
            e'8
            f'8 ]
         }
   }
   '''

   measures_decompose(t)

   r'''
   \new Voice {
         \time 1/12
         \scaleDurations #'(2 . 3) {
            c'8 [
         }
         \time 1/12
         \scaleDurations #'(2 . 3) {
            d'8
         }
         \time 1/12
         \scaleDurations #'(2 . 3) {
            e'8
         }
         \time 1/12
         \scaleDurations #'(2 . 3) {
            f'8 ]
         }
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tc'8 [\n\t\t}\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\td'8\n\t\t}\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\te'8\n\t\t}\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tf'8 ]\n\t\t}\n}"
