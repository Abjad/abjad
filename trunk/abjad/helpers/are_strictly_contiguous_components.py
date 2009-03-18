from abjad.component.component import _Component


def _are_strictly_contiguous_components(expr):
   '''True expr is a Python list of strictly contiguous components.
      Otherwise False.'''

   if not isinstance(expr, list):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, _Component):
         return False
      if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
         return False
      prev = cur

   return True
