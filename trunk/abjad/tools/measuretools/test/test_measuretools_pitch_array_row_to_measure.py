from abjad import *


def test_measuretools_pitch_array_row_to_measure_01( ):

   array = pitchtools.PitchArray([
      [1, (2, 1), ([-2, -1.5], 2)],
      [(7, 2), (6, 1), 1],
      ])

   '''
   [  ] [d'] [bf bqf    ]
   [g'     ] [fs'   ] [ ]
   '''
   measure = measuretools.pitch_array_row_to_measure(array.rows[0])

   r'''
   {
           \time 4/8
           r8
           d'8
           <bf bqf>4
   }
   '''

   assert check.wf(measure)
   assert measure.format == "{\n\t\\time 4/8\n\tr8\n\td'8\n\t<bf bqf>4\n}"
