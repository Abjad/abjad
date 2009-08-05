from abjad import *


def test_label_measure_numbers_01( ):
   '''Label measure numbers with comments before and after
   each measure.
   '''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   label.measure_numbers(t, 'comment')

   r'''
   \new Staff {
           % start measure 1
           {
                   \time 2/8
                   c'8
                   d'8
           }
           % stop measure 1
           % start measure 2
           {
                   \time 2/8
                   e'8
                   f'8
           }
           % stop measure 2
           % start measure 3
           {
                   \time 2/8
                   g'8
                   a'8
           }
           % stop measure 3
   }
   '''

   assert t.format == "\\new Staff {\n\t% start measure 1\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t% stop measure 1\n\t% start measure 2\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n\t% stop measure 2\n\t% start measure 3\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n\t% stop measure 3\n}"


def test_label_measure_numbers_02( ):
   '''Turn measure number labelling off with None.'''

   t = Staff(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   label.measure_numbers(t, 'comment')
   label.measure_numbers(t, None)

   r'''
   \new Staff {
           {
                   \time 2/8
                   c'8
                   d'8
           }
           {
                   \time 2/8
                   e'8
                   f'8
           }
           {
                   \time 2/8
                   g'8
                   a'8
           }
   }
   '''

   assert t.format == "\\new Staff {\n\t{\n\t\t\\time 2/8\n\t\tc'8\n\t\td'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\te'8\n\t\tf'8\n\t}\n\t{\n\t\t\\time 2/8\n\t\tg'8\n\t\ta'8\n\t}\n}"
