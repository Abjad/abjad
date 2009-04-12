from abjad import *


def test_container_splinter_01( ):
   '''Splinter triplet.'''

   t = Voice(FixedDurationTuplet((2, 8), run(3)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

   r'''
   \new Voice {
           \times 2/3 {
                   c'8
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8
                   g'8
                   a'8
           }
   }
   '''

   container_splinter(t[1], 1)

   r'''\new Voice {
           \times 2/3 {
                   c'8 [
                   d'8
                   e'8
           }
           \times 2/3 {
                   f'8 ]
           }
           \times 2/3 {
                   g'8 [
                   a'8 ]
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\\times 2/3 {\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t}\n\t\\times 2/3 {\n\t\tf'8 ]\n\t}\n\t\\times 2/3 {\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"


def test_container_splinter_02( ):
   '''Hew binary measure.'''

   t = Voice(RigidMeasure((3, 8), run(3)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

   r'''
   \new Voice {
                   \time 3/8
                   c'8 [
                   d'8
                   e'8
                   \time 3/8
                   f'8
                   g'8
                   a'8 ]
   }
   '''

   container_splinter(t[1], 1)

   r'''
   \new Voice {
                   \time 3/8
                   c'8 [
                   d'8
                   e'8
                   \time 1/8
                   f'8 ]
                   \time 2/8
                   g'8 [
                   a'8 ]
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\t\\time 3/8\n\t\tc'8 [\n\t\td'8\n\t\te'8\n\t\t\\time 1/8\n\t\tf'8 ]\n\t\t\\time 2/8\n\t\tg'8 [\n\t\ta'8 ]\n}"


def test_container_splinter_03( ):
   '''Hew nonbinary measure.'''

   t = Voice(RigidMeasure((3, 9), run(3)) * 2)
   pitchtools.diatonicize(t)
   p = Beam(t[:])

   r'''
   \new Voice {
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           c'8 [
                           d'8
                           e'8
                   }
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           f'8
                           g'8
                           a'8 ]
                   }
   }
   '''

   container_splinter(t[1], 1)

   r'''
   \new Voice {
                   \time 3/9
                   \scaleDurations #'(8 . 9) {
                           c'8 [
                           d'8
                           e'8
                   }
                   \time 1/9
                   \scaleDurations #'(8 . 9) {
                           f'8 ]
                   }
                   \time 2/9
                   \scaleDurations #'(8 . 9) {
                           g'8 [
                           a'8 ]
                   }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\t\\time 3/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t\t\\time 1/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tf'8 ]\n\t\t}\n\t\t\\time 2/9\n\t\t\\scaleDurations #'(8 . 9) {\n\t\t\tg'8 [\n\t\t\ta'8 ]\n\t\t}\n}"
