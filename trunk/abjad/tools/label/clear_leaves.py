from abjad.tools import iterate


def clear_leaves(expr):
   r'''Remove markup from all leaves in `expr`.

   ::

      abjad> staff = Staff(construct.scale(4))
      abjad> label.leaf_pcs(staff)
      \new Staff {
              c'8 _ \markup { \small 0 }
              d'8 _ \markup { \small 2 }
              e'8 _ \markup { \small 4 }
              f'8 _ \markup { \small 5 }
      }

   ::

      abjad> label.clear_leaves(staff)
      abjad> f(staff)
      \new Staff {
              c'8
              d'8
              e'8
              f'8
      }
   '''

   from abjad.leaf import _Leaf
   for leaf in iterate.naive_forward(expr, _Leaf):
      leaf.markup.up = [ ]
      leaf.markup.down = [ ]   
