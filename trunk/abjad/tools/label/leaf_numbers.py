from abjad.tools import iterate


def leaf_numbers(expr):
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
   '''

   from abjad.leaf import _Leaf
   for i, leaf in enumerate(iterate.naive_forward(expr, _Leaf)):
      leaf_number = i + 1
      label = r'\small %s' % leaf_number
      leaf.markup.down.append(label)
