from abjad import *


def test_construct_skips_with_multipliers_01( ):

   staff = Staff(construct.skips_with_multipliers(
      Rational(1, 4), [(1, 2), (1, 3), (1, 4), (1, 5)]))

   r'''
   \new Staff {
           s4 * 2
           s4 * 4/3
           s4 * 1
           s4 * 4/5
   }
   '''
   
   assert check.wf(staff)
   assert staff.format == '\\new Staff {\n\ts4 * 2\n\ts4 * 4/3\n\ts4 * 1\n\ts4 * 4/5\n}'
