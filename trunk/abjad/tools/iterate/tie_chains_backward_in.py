from abjad.leaf import _Leaf
from abjad.tools.iterate.naive_backward import naive_backward


def tie_chains_backward_in(expr):
   r'''Yield right-to-left tie chains in `expr`.

   ::

      abjad> notes construct.notes([0], [(5, 16), (1, 8), (1, 8), (5, 16)])
      abjad> staff = Staff(notes)
      abjad> tuplet = FixedDurationTuplet((2, 16), staff[1:3])
      abjad> pitchtools.diatonicize(staff)
      abjad> print staff.format
      \new Staff {
              c'4 ~
              \times 2/3 {
                      c'16
                      d'8
              }
              e'8
              f'4 ~
              f'16
      }

   ::

      abjad> for x in iterate.tie_chains_backward_in(t):
      ...     x
      ... 
      (Note(f', 4), Note(f', 16))
      (Note(e', 8),)
      (Note(d', 8),)
      (Note(c', 4), Note(c', 16))

   Note that one-note tie chains yield the same as other tie chains.

   Note also that nested structures are no problem.
   '''

   for leaf in naive_backward(expr, _Leaf):
      if not leaf.tie.spanned or leaf.tie.first:
         yield leaf.tie.chain
