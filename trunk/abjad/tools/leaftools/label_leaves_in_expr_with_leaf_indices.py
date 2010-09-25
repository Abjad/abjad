from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr


def label_leaves_in_expr_with_leaf_indices(expr, markup_direction = 'down'):
   r'''Label leaf indices in `expr` from 0.

   ::

      abjad> staff = Staff(macros.scale(4))
      abjad> leaftools.label_leaves_in_expr_with_leaf_indices(staff)
      \new Staff {
              c'8 _ \markup { \small 0 }
              d'8 _ \markup { \small 1 }
              e'8 _ \markup { \small 2 }
              f'8 _ \markup { \small 3 }
      } 

   .. versionadded:: 1.1.2
      new `markup_direction` keyword parameter.

   .. versionchanged:: 1.1.2
      renamed ``label.leaf_indices( )`` to
      ``leaftools.label_leaves_in_expr_with_leaf_indices( )``.
   '''

   for i, leaf in enumerate(iterate_leaves_forward_in_expr(expr)):
      label = r'\small %s' % i
      if markup_direction == 'down':
         leaf.markup.down.append(label)
      elif markup_direction == 'up':
         leaf.markup.up.append(label)
      else:
         raise ValueError("must be 'up' or 'down'.")
