from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def label_leaves_in_expr_with_leaf_depth(expr, markup_direction = 'down'):
   r'''Label the depth of every leaf in `expr`.

   ::

      abjad> staff = Staff(macros.scale(5))
      abjad> tuplettools.FixedDurationTuplet((2, 8), staff[-3:])
      abjad> leaftools.label_leaves_in_expr_with_leaf_depth(staff)
      \new Staff {
              c'8 _ \markup { \small 1 }
              d'8 _ \markup { \small 1 }
              \times 2/3 {
                      e'8 _ \markup { \small 2 }
                      f'8 _ \markup { \small 2 }
                      g'8 _ \markup { \small 2 }
              }
      }

   .. versionchanged:: 1.1.2
      renamed ``label.leaf_depth( )`` to
      ``leaftools.label_leaves_in_expr_with_leaf_depth( )``.

   .. versionchanged:: 1.1.2
      renamed ``leaftools.label_leaves_in_expr_with_score_depth( )`` to
      ``leaftools.label_leaves_in_expr_with_leaf_depth( )``.
   '''

   for leaf in iterate_leaves_forward_in_expr(expr):
      label = r'\small %s' % leaf.parentage.depth
      #leaf.markup.down.append(label)
      markup_list = getattr(leaf.markup, markup_direction)
      markup_list.append(label)
