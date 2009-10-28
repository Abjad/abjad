from abjad.tools import iterate
from abjad.tools import scoretools
from abjad.tuplet.tuplet import _Tuplet


def slip_trivial(expr):
   r'''Iterate *expr*. Slip each trivial tuplet in expr out of score.

      Arguments:
         *expr* : Abjad Component
            All trivial tuplets found in *expr* are replaced with plain leaves.

      Returns:
         None

      Example::

         abjad> t = FixedDurationTuplet((1, 4), construct.scale(3))
         abjad> u = FixedDurationTuplet((1, 4), construct.scale(2))
         abjad> s = Staff([t, u])
         abjad> len(s)
         2
         abjad> s[0]
         FixedDurationTuplet(1/4, [c'8, d'8, e'8])
         abjad> s[1]
         FixedDurationTuplet(1/4, [c'8, d'8])
         abjad> tuplettools.slip_trivial(s)
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
         }'''
   
   for tuplet in list(iterate.naive_forward(expr, _Tuplet)):
      if tuplet.trivial:
         scoretools.bequeath([tuplet], tuplet[:])
