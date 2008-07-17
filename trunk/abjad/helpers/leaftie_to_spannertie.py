from abjad.containers.container import Container
from abjad.leaf.leaf import _Leaf
from abjad.tie.spanner import Tie

def _leaftie_to_spannertie(expr):
   '''Replace all instances of Leaf.tie with a single Tie spanner.'''
   def find_contiguous_ties(leaf):
      result =  [ ]
      if not leaf.tie.isTied( ):
         return result
      prev = leaf.prev
      while prev and prev.tie.isTied( ):
         result.append(prev)
         prev = prev.prev
      next = leaf
      while next and next.tie.isTied( ):
         result.append(next)
         next = next.next
      return result

   if isinstance(expr, Container):
      for e in expr:
         _leaftie_to_spannertie(e)
   elif isinstance(expr, _Leaf):
      tied = find_contiguous_ties(expr)
      for l in tied:
         l.tie = None
         if l.tie.spanner:
            for ts in l.tie.spanners:
               ts.die( )
      Tie(tied)

