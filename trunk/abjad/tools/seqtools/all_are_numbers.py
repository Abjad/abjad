import numbers


def all_are_numbers(expr):
   '''.. versionadded:: 1.1.1

   True when `expr` is a sequence and all elements in `expr` are numbers::

      abjad> from abjad.tools import seqtools

   ::

      abjad> seqtools.all_are_numbers([1, 2, 3.0, Fraction(13, 8)])
      True

   True when `expr` is an empty sequence::

      abjad> seqtools.all_are_numbers([ ])
      True

   False otherwise::

      abjad> seqtools.all_are_numbers(17)
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.is_numeric( )`` to
      ``seqtools.all_are_numbers( )``.
   '''

   try:
      return all([isinstance(x, numbers.Number) for x in expr])
   except TypeError:
      return False
