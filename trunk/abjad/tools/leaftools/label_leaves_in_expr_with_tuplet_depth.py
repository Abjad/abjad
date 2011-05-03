from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def label_leaves_in_expr_with_tuplet_depth(expr, markup_direction = 'down'):
   r'''.. versionadded:: 1.1.1

   Label leaves in `expr` with tuplet depth::

      abjad> staff = Staff(macros.scale(5))
      abjad> tuplettools.FixedDurationTuplet((2, 8), staff[-3:])
      abjad> leaftools.label_leaves_in_expr_with_leaf_depth_tuplet(staff)
      \new Staff {
              c'8 _ \markup { \small 0 }
              d'8 _ \markup { \small 0 }
              \times 2/3 {
                      e'8 _ \markup { \small 1 }
                      f'8 _ \markup { \small 1 }
                      g'8 _ \markup { \small 1 }
              }
      }

   Return none.

   .. versionchanged:: 1.1.2
      renamed ``label.leaf_depth_tuplet( )`` to
      ``leaftools.label_leaves_in_expr_with_tuplet_depth( )``.
   '''

   for leaf in iterate_leaves_forward_in_expr(expr):
      label = r'\small %s' % leaf._parentage.depth_tuplet
      markup_list = getattr(leaf.markup, markup_direction)
      markup_list.append(label)
