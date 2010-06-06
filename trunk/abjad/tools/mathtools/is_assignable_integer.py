from abjad.tools.mathtools.binary_string import binary_string \
   as mathtools_binary_string


def is_assignable_integer(n):
   r'''.. versionadded:: 1.1.2

   True when integer `n` can be written without
   recourse to ties. Otherwise false. ::

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

   .. versionchanged:: 1.1.2
      renamed ``mathtools.is_assignable( )`` to
      ``mathtools.is_assignable_integer( )``.
   '''

   if isinstance(n, int):
      if 0 < n:
         if not '01' in mathtools_binary_string(n):
            return True
   return False
