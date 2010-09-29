from abjad.tools.leaftools.iterate_leaves_forward_in_expr import iterate_leaves_forward_in_expr
from abjad.tools import markuptools


def label_leaves_in_expr_with_leaf_numbers(expr, markup_direction = 'down'):
   r'''Label the number of every leaf in `expr`, starting at 1.

   ::

      abjad> staff = Staff(macros.scale(4))
      abjad> leaftools.label_leaves_in_expr_with_leaf_numbers(staff)
      \new Staff {
              c'8 _ \markup { \small 1 }
              d'8 _ \markup { \small 2 }
              e'8 _ \markup { \small 3 }
              f'8 _ \markup { \small 4 }
      } 

   .. versionadded:: 1.1.2:
      new `markup_direction` keyword parameter.

   .. versionchanged:: 1.1.2
      renamed ``label.leaf_numbers( )`` to
      ``leaftools.label_leaves_in_expr_with_leaf_numbers( )``.
   '''

   for i, leaf in enumerate(iterate_leaves_forward_in_expr(expr)):
      leaf_number = i + 1
      label = r'\small %s' % leaf_number
      markuptools.Markup(label, markup_direction)(leaf)
