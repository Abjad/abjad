from abjad import *


def test_measures_grouping_beam_01( ):
   '''Apply ComplexBeam to all measures in measures;
      set p.durations equal to preprolated measure durations.'''

   t = Voice(RigidMeasure((2, 8), run(2)) * 2)
   pitchtools.diatonicize(t)
   measures_grouping_beam(t[:])

   r'''
   \new Voice {
         \time 2/8
         \set stemLeftBeamCount = #0
         \set stemRightBeamCount = #1
         c'8 [
         \set stemLeftBeamCount = #1
         \set stemRightBeamCount = #1
         d'8
         \time 2/8
         \set stemLeftBeamCount = #1
         \set stemRightBeamCount = #1
         e'8
         \set stemLeftBeamCount = #1
         \set stemRightBeamCount = #0
         f'8 ]
   }
   '''

   assert check(t)
   assert t.format == "\\new Voice {\n\t\t\\time 2/8\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #1\n\t\tc'8 [\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #1\n\t\td'8\n\t\t\\time 2/8\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #1\n\t\te'8\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #0\n\t\tf'8 ]\n}"
