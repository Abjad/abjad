from abjad import *


def test_beam_complex_measured_01( ):

   t = Staff(RigidMeasure((2, 16), construct.run(2, Rational(1, 16))) * 3)
   pitchtools.diatonicize(t)

   r'''
   \new Staff {
           {
                   \time 2/16
                   c'16
                   d'16
           }
           {
                   \time 2/16
                   e'16
                   f'16
           }
           {
                   \time 2/16
                   g'16
                   a'16
           }
   }
   '''

   beam = BeamComplexMeasured(t[:])

   r'''
   \new Staff {
           {
                   \time 2/16
                   \set stemLeftBeamCount = #0
                   \set stemRightBeamCount = #2
                   c'16 [
                   \set stemLeftBeamCount = #2
                   \set stemRightBeamCount = #1
                   d'16
           }
           {
                   \time 2/16
                   \set stemLeftBeamCount = #1
                   \set stemRightBeamCount = #2
                   e'16
                   \set stemLeftBeamCount = #2
                   \set stemRightBeamCount = #1
                   f'16
           }
           {
                   \time 2/16
                   \set stemLeftBeamCount = #1
                   \set stemRightBeamCount = #2
                   g'16
                   \set stemLeftBeamCount = #2
                   \set stemRightBeamCount = #0
                   a'16 ]
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/16\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #2\n\t\tc'16 [\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\td'16\n\t}\n\t{\n\t\t\\time 2/16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\te'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #1\n\t\tf'16\n\t}\n\t{\n\t\t\\time 2/16\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #2\n\t\tg'16\n\t\t\\set stemLeftBeamCount = #2\n\t\t\\set stemRightBeamCount = #0\n\t\ta'16 ]\n\t}\n}"
