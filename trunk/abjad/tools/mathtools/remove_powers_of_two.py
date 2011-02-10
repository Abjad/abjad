def remove_powers_of_two(n):
   r'''Remove powers of ``2`` from the factors of positive integer `n`::

      abjad> for n in range(10, 100, 10):
      ...     print '\t%s\t%s' % (n, mathtools.remove_powers_of_two(n))
      ... 
         10 5
         20 5
         30 15
         40 5
         50 25
         60 15
         70 35
         80 5
         90 45

   Raise type error on noninteger `n`::

      abjad> mathtools.remove_powers_of_two(7.5)
      TypeError

   Raise value error on nonpositive `n`::

      abjad> mathtools.remove_powers_of_two(-1)
      ValueError

   Return positive integer.
   '''

   if not isinstance(n, (int, long)):
      raise TypeError

   if n <= 0:
      raise ValueError

   while n % 2 == 0:
      n /= 2

   return n
