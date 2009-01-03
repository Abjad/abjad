from abjad import *


def test_measure_compressed_meter_grob_handling_01( ):
   '''
   Compressed measures handle meter overrides and meter reverts.
   '''

   t = Measure((4, 8), scale(3))
   t.meter.color = 'red'

   r'''
        \override TimeSignature #'color = #red
        \time 4/8
        \scaleDurations #'(4 . 3) {
                c'8
                d'8
                e'8
        }
        \revert TimeSignature #'color
   '''

   assert t.format == "\t\\override TimeSignature #'color = #red\n\t\\time 4/8\n\t\\scaleDurations #'(4 . 3) {\n\t\tc'8\n\t\td'8\n\t\te'8\n\t}\n\t\\revert TimeSignature #'color"
