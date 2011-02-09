from abjad.tools import mathtools


def all_are_nonnegative_integer_powers_of_two(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` is a sequence and all elements in `expr` are nonnegative integer powers of two::

      abjad> seqtools.all_are_nonnegative_integer_powers_of_two([0, 1, 1, 1, 2, 4, 32, 32])
      True

   True when `expr` is an empty sequence::

      abjad> seqtools.all_are_nonnegative_integer_powers_of_two([ ])
      True

   False otherwise::

      abjad> seqtools.all_are_nonnegative_integer_powers_of_two(17)
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.all_are_powers_of_two( )`` to
      ``seqtools.all_are_nonnegative_integer_powers_of_two( )``.
   '''

   try:
      return all([mathtools.is_nonnegative_integer_power_of_two(x) for x in expr])
   except TypeError:
      return False
