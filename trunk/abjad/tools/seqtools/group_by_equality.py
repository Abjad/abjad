import itertools


def group_by_equality(l):
   '''Group elements in `l` by equality::

      abjad> l = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]

   ::
   
      abjad> list(seqtools.group_by_equality(l))
      [(0, 0), (-1, -1), (2,), (3,), (-5,), (1, 1), (5,), (-5,)] 

   Return generator of tuples.
   '''

   g = itertools.groupby(l, lambda x: x)
   for n, group in g:
      yield tuple(group)
