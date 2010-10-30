from abjad.tools.mathtools.integer_to_binary_string import integer_to_binary_string


def is_assignable_integer(expr):
   r'''.. versionadded:: 1.1.2

   True when `expr` is equivalent to an integer and 
   can be written without recourse to ties::

      abjad> for n in range(0, 16 + 1):
      ...     print '%s\t%s' % (n, mathtools.is_assignable_integer(n))
      ... 
      0  False
      1  True
      2  True
      3  True
      4  True
      5  False
      6  True
      7  True
      8  True
      9  False
      10 False
      11 False
      12 True
      13 False
      14 True
      15 True
      16 True

   Otherwise false.

   Return boolean.

   .. versionchanged:: 1.1.2
      renamed ``mathtools.is_assignable( )`` to
      ``mathtools.is_assignable_integer( )``.
   '''

   if isinstance(expr, int):
      if 0 < expr:
         if not '01' in integer_to_binary_string(expr):
            return True
   return False
