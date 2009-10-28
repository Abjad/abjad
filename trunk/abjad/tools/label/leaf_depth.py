from abjad.tools import iterate


def leaf_depth(expr):
   r'''Label the depth of every leaf in `expr`.

   ::

      abjad> staff = Staff(construct.scale(5))
      abjad> FixedDurationTuplet((2, 8), staff[-3:])
      abjad> label.leaf_depth(staff)
      \new Staff {
              c'8 _ \markup { \small 1 }
              d'8 _ \markup { \small 1 }
              \times 2/3 {
                      e'8 _ \markup { \small 2 }
                      f'8 _ \markup { \small 2 }
                      g'8 _ \markup { \small 2 }
              }
      }
   '''

   from abjad.leaf.leaf import _Leaf
   for leaf in iterate.naive_forward(expr, _Leaf):
      label = r'\small %s' % leaf.parentage.depth
      leaf.markup.down.append(label)
