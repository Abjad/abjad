from abjad import *


def test_measuretools_beam_01( ):
   '''Beam all measures in expr with plain old Beam spanner.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   measuretools.beam(t, style = None)

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8 [
                   d'8 ]
           }
           {
                   \time 2/8
                   e'8 [
                   f'8 ]
           }
           {
                   \time 2/8
                   g'8 [
                   a'8 ]
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8 [\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8 [\n\t\tf'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8 [\n\t\ta'8 ]\n\t}\n}"


def test_measuretools_beam_02( ):
   '''Beam all measures in expr with BeamComplexDurated.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 2)
   pitchtools.diatonicize(t)
   measuretools.beam(t, style = 'complex')

   r'''
   \new Staff {
           {
                   \time 2/8
                   \set stemLeftBeamCount = #0
                   \set stemRightBeamCount = #1
                   c'8 [
                   \set stemLeftBeamCount = #1
                   \set stemRightBeamCount = #0
                   d'8 ]
           }
           {
                   \time 2/8
                   \set stemLeftBeamCount = #0
                   \set stemRightBeamCount = #1
                   e'8 [
                   \set stemLeftBeamCount = #1
                   \set stemRightBeamCount = #0
                   f'8 ]
           }
   }
   '''

   assert check.wf(t)
   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #1\n\t\tc'8 [\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #0\n\t\td'8 ]\n\t}\n\t{\n\t\t\\time 2/8\n\t\t\\set stemLeftBeamCount = #0\n\t\t\\set stemRightBeamCount = #1\n\t\te'8 [\n\t\t\\set stemLeftBeamCount = #1\n\t\t\\set stemRightBeamCount = #0\n\t\tf'8 ]\n\t}\n}"
