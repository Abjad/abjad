from abjad.tools import iterate


def leaf_indices(expr):
   r'''Label the indiex of every leaf in `expr`, starting at 0.

   ::

      abjad> staff = Staff(construct.scale(4))
      abjad> label.leaf_indices(staff)
      \new Staff {
              c'8 _ \markup { \small 0 }
              d'8 _ \markup { \small 1 }
              e'8 _ \markup { \small 2 }
              f'8 _ \markup { \small 3 }
      } 
   '''

   from abjad.leaf.leaf import _Leaf
   for i, leaf in enumerate(iterate.naive_forward(expr, _Leaf)):
      label = r'\small %s' % i
      leaf.markup.down.append(label)
