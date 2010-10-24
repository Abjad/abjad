from abjad.tools import mathtools


def get_element_at_cyclic_index(iterable, index):
   r'''.. versionadded:: 1.1.2

   Get element at nonnegative cyclic `index` in `iterable`::

      abjad> iterable = 'string'

   ::

      abjad> for index in range(10):
      ...     print '%s\t%s' % (index, listtools.get_element_at_cyclic_index(iterable, index))
      ... 
      0  s
      1  t
      2  r
      3  i
      4  n
      5  g
      6  s
      7  t
      8  r
      9  i

   Get element at negative cyclic `index` in `iterable`::

      abjad> for index in range(1, 11):
      ...     print '%s\t%s' % (-index, listtools.get_element_at_cyclic_index(iterable, -index))
      ... 
      -1    g
      -2    n
      -3    i
      -4    r
      -5    t
      -6    s
      -7    g
      -8    n
      -9    i
      -10   r

   Return element.
   '''

   return iterable[mathtools.sign(index) * (abs(index) % len(iterable))]
