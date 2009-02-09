from abjad import *


def test_measures_make_01( ):
   '''Make list of skip-populated rigid measures;
      only one skip per measure, with LilyPond
      duration multipliers, as required.'''

   t = Staff(measures_make([(1, 8), (5, 16), (5, 16), (1, 4)]))

   r'''
   \new Staff {
                   \time 1/8
                   s1 * 1/8
                   \time 5/16
                   s1 * 5/16
                   \time 5/16
                   s1 * 5/16
                   \time 1/4
                   s1 * 1/4
   }
   '''

   assert t.format == '\\new Staff {\n\t\t\\time 1/8\n\t\ts1 * 1/8\n\t\t\\time 5/16\n\t\ts1 * 5/16\n\t\t\\time 5/16\n\t\ts1 * 5/16\n\t\t\\time 1/4\n\t\ts1 * 1/4\n}'
