from abjad.component.component import _Component


def _are_strictly_contiguous_components_in_same_parent(expr):
   '''True when expr is a Python list of Abjad components such that

         1. all components in list are strictly contiguous, and
         2. every component in list has the same parent.

      Otherwise False.'''

   if isinstance(expr, list):
      if len(expr) == 0:
         return True
      first = expr[0]
      if isinstance(first, _Component):
         first_parent = first.parentage.parent
         if first_parent is None:
            return False
         prev = first
         for cur in expr[1:]:
            if not isinstance(cur, _Component):
               return False
            if not cur.parentage.parent is first_parent:
               return False
            if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
               return False
            prev = cur
         return True
   return False
