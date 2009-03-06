from abjad.helpers.bequeath_multiple import bequeath_multiple
from abjad.helpers.iterate import iterate


def tuplets_slip_trivial(expr):
   '''Iterate expr. Slip each trivial tuplet in expr out of score.
      Return None because processes potentially many trivial tuplets.'''
   
   for tuplet in list(iterate(expr, '_Tuplet')):
      if tuplet.trivial:
         bequeath_multiple([tuplet], tuplet[:])
