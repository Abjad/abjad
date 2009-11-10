from abjad.leaf import _Leaf


def is_chain(expr):
   '''True when expr is a tie chain, otherwise False.'''

   if isinstance(expr, tuple):
      length = len(expr)
      if length == 0:
         return True
      elif length == 1:
         if isinstance(expr[0], _Leaf):
            return True
      else:
         tie_spanners = set([element.tie.spanner for element in expr])
         return len(tie_spanners) == 1

   return False
