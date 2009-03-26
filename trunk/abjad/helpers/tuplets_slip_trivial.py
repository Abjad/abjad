#from abjad.helpers.bequeath_multiple import bequeath_multiple
from abjad.helpers.get_parent_and_index import get_parent_and_index
from abjad.helpers.iterate import iterate


def tuplets_slip_trivial(expr):
   '''Iterate expr. Slip each trivial tuplet in expr out of score.
      Return None because processes potentially many trivial tuplets.'''
   
   from abjad.tuplet.tuplet import _Tuplet
   for tuplet in list(iterate(expr, _Tuplet)):
      if tuplet.trivial:
         #bequeath_multiple([tuplet], tuplet[:])
         parent, index = get_parent_and_index([tuplet])
         parent[index:index+1] = tuplet[:]
