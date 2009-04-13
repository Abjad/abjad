from abjad import *


def test_containertools_shatter_01( ):
   '''Shatter binary measure in voice.'''

   t = Voice([RigidMeasure((3, 8), construct.scale(3))])
   Beam(t[0])
   containertools.shatter(t[0])

   r'''\new Voice {
         \time 1/8
         c'8 [ ]
         \time 1/8
         d'8 [ ]
         \time 1/8
         e'8 [ ]
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\t\\time 1/8\n\t\tc'8 [ ]\n\t\t\\time 1/8\n\t\td'8 [ ]\n\t\t\\time 1/8\n\t\te'8 [ ]\n}"


def test_containertools_shatter_02( ):
   '''Shatter nonbinary measure in voice.'''

   t = Voice([RigidMeasure((3, 12), construct.scale(3))])
   Beam(t[0])
   containertools.shatter(t[0])

   r'''\new Voice {
         \time 1/12
         \scaleDurations #'(2 . 3) {
            c'8 [ ]
         }
         \time 1/12
         \scaleDurations #'(2 . 3) {
            d'8 [ ]
         }
         \time 1/12
         \scaleDurations #'(2 . 3) {
            e'8 [ ]
         }
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\tc'8 [ ]\n\t\t}\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\td'8 [ ]\n\t\t}\n\t\t\\time 1/12\n\t\t\\scaleDurations #'(2 . 3) {\n\t\t\te'8 [ ]\n\t\t}\n}"


def test_containertools_shatter_03( ):
   '''Shatter nested tuplet.'''

   t = FixedDurationTuplet((2, 8), construct.run(3))
   Beam(t[:])
   donate(t[-1:], FixedDurationTuplet((1, 8), construct.scale(3, (1, 16))))
   pitchtools.diatonicize(t)

   r'''\times 2/3 {
      c'8 [
      d'8
      \times 2/3 {
         e'16
         f'16
         g'16 ]
      }
   }'''

   containertools.shatter(t[-1])

   r'''\times 2/3 {
      c'8 [
      d'8
      \times 2/3 {
         e'16 ]
      }
      \times 2/3 {
         f'16 [ ]
      }
      \times 2/3 {
         g'16 [ ]
      }
   }'''

   assert check.wf(t)
   assert t.format == "\\times 2/3 {\n\tc'8 [\n\td'8\n\t\\times 2/3 {\n\t\te'16 ]\n\t}\n\t\\times 2/3 {\n\t\tf'16 [ ]\n\t}\n\t\\times 2/3 {\n\t\tg'16 [ ]\n\t}\n}"
