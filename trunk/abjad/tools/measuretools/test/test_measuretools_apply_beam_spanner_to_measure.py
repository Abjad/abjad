from abjad import *


def test_measuretools_apply_beam_spanner_to_measure_01( ):

   measure = RigidMeasure((2, 8), construct.run(2))

   r'''
   {
        \time 2/8
        c'8
        c'8
   }
   '''

   measuretools.apply_beam_spanner_to_measure(measure)


   r'''
   {
        \time 2/8
        c'8 [
        c'8 ]
   }
   '''

   assert check.wf(measure)
   assert measure.format == "{\n\t\\time 2/8\n\tc'8 [\n\tc'8 ]\n}"
