from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def label_leaves_in_expr_with_leaf_depth(expr, markup_direction = 'down'):
   r'''.. versionadded:: 1.1.1

   Label leaves in `expr` with leaf depth::

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
   
   Return none.
   '''

   for leaf in iterate_leaves_forward_in_expr(expr):
      label = r'\small %s' % leaf._parentage.depth
      markuptools.Markup(label, markup_direction)(leaf)
