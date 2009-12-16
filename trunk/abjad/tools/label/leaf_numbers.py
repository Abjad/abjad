from abjad.tools import iterate


def leaf_numbers(expr, direction = 'below'):
   r'''Label the number of every leaf in `expr`, starting at 1.

   ::

      abjad> staff = Staff(construct.scale(4))
      abjad> label.leaf_numbers(staff)
      \new Staff {
              c'8 _ \markup { \small 1 }
              d'8 _ \markup { \small 2 }
              e'8 _ \markup { \small 3 }
              f'8 _ \markup { \small 4 }
      } 

   .. versionadded:: 1.1.2:
      new `direction` keyword parameter.
   '''

   for i, leaf in enumerate(iterate.leaves_forward_in(expr)):
      leaf_number = i + 1
      label = r'\small %s' % leaf_number
      if direction == 'below':
         leaf.markup.down.append(label)
      elif direction == 'above':
         leaf.markup.up.append(label)
      else:
         raise ValueError("must be 'above' or 'below'.")
