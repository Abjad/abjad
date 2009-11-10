from abjad.container import Container
from abjad.exceptions import TieChainError
from abjad.leaf import _Leaf


def chained_contents(expr):
   r'''Yield the left-to-right, top-level contents of `expr`
   with chain-wrapped leaves. ::

      t = Staff(construct.notes(0, [(5, 32)] * 4))
      t.insert(4, FixedDurationTuplet((2, 8), construct.run(3)))
      pitchtools.diatonicize(t)
      abjad> print t.format
      \new Staff {
         c'8 ~
         c'32
         \times 2/3 {
            d'8
            e'8
            f'8
         }
         g'8 ~
         g'32
         a'8 ~
         a'32
         b'8 ~
         b'32
      }

   ::

      abjad> for x in iterate.chained_contents(t):
      ...     x
      ... 
      (Note(c', 8), Note(c', 32))
      (Note(d', 8), Note(d', 32))
      FixedDurationTuplet(1/4, [e'8, f'8, g'8])
      (Note(a', 8), Note(a', 32))
      (Note(b', 8), Note(b', 32))

   Crossing ties raise :exc:`TieChainError`.
   '''

   if isinstance(expr, _Leaf):
      if len(expr.tie.chain) == 1:
         yield expr.tie.chain
      else:
         raise TieChainError('can not only one leaf in tie chain.')
   elif isinstance(expr, (list, Container)):
      for component in expr:
         if isinstance(component, _Leaf):
            if not component.tie.spanned or component.tie.last:
               yield component.tie.chain
         elif isinstance(component, Container):
            yield component
   else:
      raise ValueError('input must be iterable.')
