#from abjad.tools.leaftools.group_by_leaf_type import group_by_leaf_type
from abjad.tools.iterate.group_by_type_and_yield_groups import \
   group_by_type_and_yield_groups


def group_by_type_and_yield_groups_of_klass(expr, klass):
   '''.. versionadded:: 1.1.2

   Group elements in `expr` by type and yield only those
   groups with all elements of `klass`::

      staff = Staff(construct.leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
      abjad> for x in leaftools.subruns_of_type(staff, Note):
      ...     x
      ... 
      (Note(c', 8), Note(d', 8), Note(e', 8))
      (Note(f', 8), Note(g', 8))

   .. versionchanged:: 1.1.2
      renamed ``leaftools.subruns_of_type( )`` to
      ``iterate.group_by_type_and_yield_groups_of_klass( )``.
   '''

   for group in group_by_type_and_yield_groups(expr):
      if isinstance(group[0], klass):
         yield group
