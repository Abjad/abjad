from abjad.tools.leaftools.group_by_leaf_type import group_by_leaf_type


def subruns_of_type(expr, klass):
   '''.. versionadded:: 1.1.2

   Yield tuples of contiguous elements of `klass` in `expr`. ::

      staff = Staff(construct.leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
      abjad> for x in leaftools.subruns_of_type(staff, Note):
      ...     x
      ... 
      (Note(c', 8), Note(d', 8), Note(e', 8))
      (Note(f', 8), Note(g', 8))
   '''

   for group in group_by_leaf_type(expr):
      if isinstance(group[0], klass):
         yield group
