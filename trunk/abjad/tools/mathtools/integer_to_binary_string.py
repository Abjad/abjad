def integer_to_binary_string(n):
   r'''Return the base-2 representation of positive integer `n` 
   as a string. ::

      abjad> mathtools.integer_to_binary_string(5)
      '101'
   
   ::

      abjad> for n in range(1, 17):
      ...     print '\t%s\t%s' % (n, mathtools.integer_to_binary_string(n))
      ... 
         1  1
         2  10
         3  11
         4  100
         5  101
         6  110
         7  111
         8  1000
         9  1001
         10 1010
         11 1011
         12 1100
         13 1101
         14 1110
         15 1111
         16 10000

   .. note:: ``mathtools.integer_to_binary_string(n)`` will deprecate when \
      Abjad migrates to Python 2.6.

   .. versionchanged:: 1.1.2
      renamed ``mathtools.binary_string( )`` to
      ``mathtools.integer_to_binary_string( )``.
   '''

   if not isinstance(n, (int, long)):
      raise TypeError

   result = ''
   while n > 0:
      result = str(n % 2) + result
      n = n >> 1

   return result
