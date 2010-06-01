import itertools


def group_by_leaf_type(leaves):
   '''.. versionadded:: 1.1.2

   Yield successive tuples from `leaves` by type::

      abjad> staff = Staff(construct.leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
      abjad> for x in leaftools.group_by_leaf_type(staff):
      ...     x
      ... 
      (Note(c', 8), Note(d', 8), Note(e', 8))
      (Rest(8), Rest(8))
      (Note(f', 8), Note(g', 8))
   '''

   grouper = itertools.groupby(leaves, type)
   for leaf_type, generator in grouper:
      yield tuple(generator)
