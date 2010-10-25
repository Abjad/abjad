import numbers


def all_are_numbers(sequence):
   '''.. versionadded:: 1.1.1

   True when all elements in `sequence` are numbers::

      abjad> listtools.all_are_numbers([1, 2, 3.0, Fraction(13, 8)])
      True

   True when on empty `sequence`::

      abjad> listtools.all_are_numbers([ ])
      True

   False otherwise::

      abjad> listtools.all_are_numbers([1, 2, 3, 'string'])
      False

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``listtools.is_numeric( )`` to
      ``listtools.all_are_numbers( )``.
   '''

   #return all([isinstance(x, (int, long, float, Fraction)) for x in l])
   return all([isinstance(x, numbers.Number) for x in sequence])
