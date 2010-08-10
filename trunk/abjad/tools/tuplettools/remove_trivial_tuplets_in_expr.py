from abjad.tools import componenttools
from abjad.tools import iterate
from abjad.components._Tuplet import _Tuplet


def remove_trivial_tuplets_in_expr(expr):
   r'''Iterate `expr`. Slip each trivial tuplet in expr out of score.

   Arguments:
      `expr` : Abjad Component
         All trivial tuplets found in `expr` are replaced with plain leaves.

   Returns:
      None

   Example::

      abjad> t = FixedDurationTuplet((1, 4), macros.scale(3))
      abjad> u = FixedDurationTuplet((1, 4), macros.scale(2))
      abjad> s = Staff([t, u])
      abjad> len(s)
      2
      abjad> s[0]
      FixedDurationTuplet(1/4, [c'8, d'8, e'8])
      abjad> s[1]
      FixedDurationTuplet(1/4, [c'8, d'8])
      abjad> tuplettools.remove_trivial_tuplets_in_expr(s)
      abjad> len(s)
      3
      abjad> s[0]
      FixedDurationTuplet(1/4, [c'8, d'8, e'8])
      abjad> s[1]
      Note(c', 8)
      abjad> s[2]
      Note(d', 8)
      abjad> f(s)
      \new Staff {
              \times 2/3 {
                      c'8
                      d'8
                      e'8
              }
              c'8
              d'8
      }

   .. versionchanged:: 1.1.2
      renamed ``tuplettools.slip_trivial( )`` to
      ``tuplettools.remove_trivial_tuplets_in_expr( )``.
   '''
   
   for tuplet in list(componenttools.iterate_components_forward_in_expr(expr, _Tuplet)):
      if tuplet.trivial:
         componenttools.move_parentage_and_spanners_from_components_to_components([tuplet], tuplet[:])
