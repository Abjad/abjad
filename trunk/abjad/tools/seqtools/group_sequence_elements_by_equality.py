import itertools


def group_sequence_elements_by_equality(l):
   '''Group elements in `l` by equality::

      abjad> l = [0, 0, -1, -1, 2, 3, -5, 1, 1, 5, -5]

   ::
   
      abjad> list(seqtools.group_sequence_elements_by_equality(l))
      [(0, 0), (-1, -1), (2,), (3,), (-5,), (1, 1), (5,), (-5,)] 

   Return generator of tuples.

   .. versionchanged:: 1.1.2
      renamed ``seqtools.group_by_equality( )`` to
      ``seqtools.group_sequence_elements_by_equality( )``.
   '''

   g = itertools.groupby(l, lambda x: x)
   for n, group in g:
      yield tuple(group)
