from abjad.helpers.remove_powers_of_two import _remove_powers_of_two


def test_remove_powers_of_two_01( ):
   '''Remove powers of two from integer n.'''

   assert _remove_powers_of_two(10) == 5
   assert _remove_powers_of_two(20) == 5
   assert _remove_powers_of_two(30) == 15
   assert _remove_powers_of_two(40) == 5
   assert _remove_powers_of_two(50) == 25
   assert _remove_powers_of_two(60) == 15
   assert _remove_powers_of_two(70) == 35
   assert _remove_powers_of_two(80) == 5
   assert _remove_powers_of_two(90) == 45
