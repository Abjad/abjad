from abjad import *


def test_measuretools_decompose_01( ):
   '''Decompose binary measures in voice.'''

   t = Voice(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[:])

   r'''\new Voice {
         \time 2/8
         c'8 [
         d'8
         \time 2/8
         e'8
         f'8 ]
   }'''

   measuretools.decompose(t)

   r'''\new Voice {
         \time 1/8
         c'8 [
         \time 1/8
         d'8
         \time 1/8
         e'8
         \time 1/8
         f'8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\t\\time 1/8\n\t\tc'8 [\n\t\t\\time 1/8\n\t\td'8\n\t\t\\time 1/8\n\t\te'8\n\t\t\\time 1/8\n\t\tf'8 ]\n}"


def test_measuretools_decompose_02( ):
   '''Decompose nonbinary measures in voice.'''

   t = Voice(RigidMeasure((2, 12), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t[:])

   r'''\new Voice {
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
   }'''

   measuretools.decompose(t)

   r'''\new Voice {
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
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tc'8 [\n\t\t}\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\td'8\n\t\t}\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\te'8\n\t\t}\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tf'8 ]\n\t\t}\n}"


def test_measuretools_decompose_03( ):
   '''Decompose binary measure containing tuplets.'''

   t = Voice(RigidMeasure((3, 8), [
      FixedDurationTuplet((2, 8), construct.run(3)), Note(0, (1, 8))]) * 2)
   pitchtools.diatonicize(t)
   Beam(t.leaves)

   r'''\new Voice {
         \time 3/8
         \times 2/3 {
            c'8 [
            d'8
            e'8
         }
         f'8
         \time 3/8
         \times 2/3 {
            g'8
            a'8
            b'8
         }
         c''8 ]
   }'''

   measuretools.decompose(t)

   r'''\new Voice {
         \time 2/8
         \times 2/3 {
            c'8 [
            d'8
            e'8
         }
         \time 1/8
         f'8
         \time 2/8
         \times 2/3 {
            g'8
            a'8
            b'8
         }
         \time 1/8
         c''8 ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\t\\time 2/8\n\t\t\\times 2/3 {\n\t\t\tc'8 [\n\t\t\td'8\n\t\t\te'8\n\t\t}\n\t\t\\time 1/8\n\t\tf'8\n\t\t\\time 2/8\n\t\t\\times 2/3 {\n\t\t\tg'8\n\t\t\ta'8\n\t\t\tb'8\n\t\t}\n\t\t\\time 1/8\n\t\tc''8 ]\n}"
