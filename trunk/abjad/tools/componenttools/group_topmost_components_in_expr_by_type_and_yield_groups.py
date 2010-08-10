import itertools


def group_topmost_components_in_expr_by_type_and_yield_groups(expr):
   '''.. versionadded:: 1.1.2

   Group elements in `expr` by type and yield groups::

      abjad> staff = Staff(leaftools.make_leaves([0, 2, 4, None, None, 5, 7], [(1, 8)]))
      abjad> for x in componenttools.group_topmost_components_in_expr_by_type_and_yield_groups(staff):
      ...     x
      ... 
      (Note(c', 8), Note(d', 8), Note(e', 8))
      (Rest(8), Rest(8))
      (Note(f', 8), Note(g', 8))

   .. versionchanged:: 1.1.2
      renamed ``leaftools.group_by_leaf_type( )`` to
      ``componenttools.group_topmost_components_in_expr_by_type_and_yield_groups( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.group_by_type_and_yield_groups( )`` to
      ``componenttools.group_topmost_components_in_expr_by_type_and_yield_groups( )``.

   .. versionchanged:: 1.1.2
      renamed ``iterate.group_topmost_components_in_expr_by_type_and_yield_groups( )`` to
      ``componenttools.group_topmost_components_in_expr_by_type_and_yield_groups( )``.
   '''

   grouper = itertools.groupby(expr, type)
   for leaf_type, generator in grouper:
      yield tuple(generator)
