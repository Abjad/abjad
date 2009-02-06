from abjad.helpers.next_least_power_of_two import _next_least_power_of_two
import py.test


def test_next_least_power_of_two_01( ):
   '''Return greatest integer power of two
      less than or equal to n.'''

   assert _next_least_power_of_two(1) == 1
   assert _next_least_power_of_two(2) == 2
   assert _next_least_power_of_two(3) == 2
   assert _next_least_power_of_two(4) == 4
   assert _next_least_power_of_two(5) == 4
   assert _next_least_power_of_two(6) == 4
   assert _next_least_power_of_two(7) == 4
   assert _next_least_power_of_two(8) == 8
   assert _next_least_power_of_two(9) == 8
   assert _next_least_power_of_two(10) == 8
   assert _next_least_power_of_two(11) == 8
   assert _next_least_power_of_two(12) == 8


def test_next_least_power_of_two_02( ):
   '''Gives OverflowError on 0.'''

   assert py.test.raises(OverflowError, '_next_least_power_of_two(0)')
