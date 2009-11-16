from abjad.tools import iterate


def leaf_depth_tuplet(expr):
   r'''Label the tuplet depth of every leaf in `expr`.

   ::

      abjad> staff = Staff(construct.scale(5))
      abjad> FixedDurationTuplet((2, 8), staff[-3:])
      abjad> label.leaf_depth_tuplet(staff)
      \new Staff {
              c'8 _ \markup { \small 0 }
              d'8 _ \markup { \small 0 }
              \times 2/3 {
                      e'8 _ \markup { \small 1 }
                      f'8 _ \markup { \small 1 }
                      g'8 _ \markup { \small 1 }
              }
      }
   '''

   for leaf in iterate.leaves_forward_in(expr):
      label = r'\small %s' % leaf.parentage.depth_tuplet
      leaf.markup.down.append(label)
