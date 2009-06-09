from abjad import *
import py.test


def test_next_least_power_of_two_01( ):
   '''Return greatest integer power of two
      less than or equal to n.'''

   assert mathtools.next_least_power_of_two(1) == 1
   assert mathtools.next_least_power_of_two(2) == 2
   assert mathtools.next_least_power_of_two(3) == 2
   assert mathtools.next_least_power_of_two(4) == 4
   assert mathtools.next_least_power_of_two(5) == 4
   assert mathtools.next_least_power_of_two(6) == 4
   assert mathtools.next_least_power_of_two(7) == 4
   assert mathtools.next_least_power_of_two(8) == 8
   assert mathtools.next_least_power_of_two(9) == 8
   assert mathtools.next_least_power_of_two(10) == 8
   assert mathtools.next_least_power_of_two(11) == 8
   assert mathtools.next_least_power_of_two(12) == 8


def test_next_least_power_of_two_02( ):
   '''Raise TypeError on nonnumeric n.
      Raise ValueError on nonpositive n.'''

   assert py.test.raises(TypeError, "mathtools.next_least_power_of_two('foo')")
   assert py.test.raises(ValueError, 'mathtools.next_least_power_of_two(0)')
   assert py.test.raises(ValueError, 'mathtools.next_least_power_of_two(-1)')


def test_next_least_power_of_two_03( ):
   '''Optional offset keyword allows for the next to greatest
      integer power of two, etc.'''

   assert mathtools.next_least_power_of_two(1, 1) == 0.5
   assert mathtools.next_least_power_of_two(2, 1) == 1
   assert mathtools.next_least_power_of_two(3, 1) == 1
   assert mathtools.next_least_power_of_two(4, 1) == 2
   assert mathtools.next_least_power_of_two(5, 1) == 2
   assert mathtools.next_least_power_of_two(6, 1) == 2
   assert mathtools.next_least_power_of_two(7, 1) == 2
   assert mathtools.next_least_power_of_two(8, 1) == 4
   assert mathtools.next_least_power_of_two(9, 1) == 4
   assert mathtools.next_least_power_of_two(10, 1) == 4
   assert mathtools.next_least_power_of_two(11, 1) == 4
   assert mathtools.next_least_power_of_two(12, 1) == 4
