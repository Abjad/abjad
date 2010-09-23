from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def label_leaves_in_expr_with_tuplet_depth(expr):
   r'''Label the tuplet depth of every leaf in `expr`.

   ::

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

   .. versionchanged:: 1.1.2
      renamed ``label.leaf_depth_tuplet( )`` to
      ``leaftools.label_leaves_in_expr_with_tuplet_depth( )``.
   '''

   for leaf in iterate_leaves_forward_in_expr(expr):
      label = r'\small %s' % leaf.parentage.depth_tuplet
      leaf.markup.down.append(label)
