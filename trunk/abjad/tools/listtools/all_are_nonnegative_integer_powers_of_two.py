from abjad.tools import mathtools


def all_are_nonnegative_integer_powers_of_two(sequence):
   '''.. versionadded:: 1.1.2

   True when all elements in `sequence` are nonnegative integer powers of two::

      abjad> listtools.all_are_nonnegative_integer_powers_of_two([0, 1, 1, 1, 2, 4, 32, 32])
      True

   True on empty `sequence`::

      abjad> listtools.all_are_nonnegative_integer_powers_of_two([ ])
      True

   False otherwise::

      abjad> listtools.all_are_nonnegative_integer_powers_of_two([1, 1, 3, 9, 27, 27])
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``listtools.all_are_powers_of_two( )`` to
      ``listtools.all_are_nonnegative_integer_powers_of_two( )``.
   '''

   return all([mathtools.is_nonnegative_integer_power_of_two(x) for x in sequence])
