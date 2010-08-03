from abjad.components._Leaf import _Leaf
from abjad.tools.iterate.naive_forward_in_expr import naive_forward_in_expr


def tie_chains_forward_in_expr(expr):
   r'''Yield left-to-right tie chains in `expr`.

   ::

      abjad> notes leaftools.make_notes([0], [(5, 16), (1, 8), (1, 8), (5, 16)])
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

      abjad> for x in iterate.tie_chains_forward_in_expr(t):
      ...     x
      ... 
      (Note(c', 4), Note(c', 16))
      (Note(d', 8),)
      (Note(e', 8),)
      (Note(f', 4), Note(f', 16))

   Note that one-note tie chains yield the same as other tie chains.

   Note also that nested structures are no problem.

   .. versionchanged:: 1.1.2
      renamed ``iterate.tie_chains_forward_in( )`` to
      ``iterate.tie_chains_forward_in_expr( )``.
   '''

   for leaf in naive_forward_in_expr(expr, _Leaf):
      if not leaf.tie.spanned or leaf.tie.last:
         yield leaf.tie.chain
