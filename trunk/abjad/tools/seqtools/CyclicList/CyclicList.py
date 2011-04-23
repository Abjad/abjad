class CyclicList(list):
   '''.. versionadded:: 1.1.2

   Abjad model of cyclic list::

      abjad> cyclic_list = seqtools.CyclicList('abcd')

   ::

      abjad> cyclic_list
      ['a', 'b', 'c', 'd']

   ::

      abjad> for x in range(8):
      ...     print x, cyclic_list[x]
      ... 
      0 a
      1 b
      2 c
      3 d
      4 a
      5 b
      6 c
      7 d

   Cyclic lists overload the item-getting method of built-in lists.

   Cyclic lists return a value for any integer index.

   Cyclic lists otherwise behave exactly like built-in lists.
   '''

   ## OVERLOADS ##

   def __getitem__(self, expr):
      return list.__getitem__(self, expr % len(self))

   def __getslice__(self, start_index, stop_index):
      result = [ ]
      result = [self[n] for n in range(start_index, stop_index)]
      return result
