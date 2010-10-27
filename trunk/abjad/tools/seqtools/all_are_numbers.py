import numbers


def all_are_numbers(sequence):
   '''.. versionadded:: 1.1.1

   True when all elements in `sequence` are numbers::

      abjad> seqtools.all_are_numbers([1, 2, 3.0, Fraction(13, 8)])
      True

   True when on empty `sequence`::

      abjad> seqtools.all_are_numbers([ ])
      True

   False otherwise::

      abjad> seqtools.all_are_numbers([1, 2, 3, 'string'])
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.is_numeric( )`` to
      ``seqtools.all_are_numbers( )``.
   '''

   #return all([isinstance(x, (int, long, float, Fraction)) for x in l])
   return all([isinstance(x, numbers.Number) for x in sequence])
