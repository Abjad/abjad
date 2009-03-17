from abjad.component.component import _Component


def _are_successive_containerized_components(expr):
   '''True when expr is a Python list and when

         1. every element in list is an Abjad component,
         2. every component in list has a parent,
         3. every component in list has the same parent
         4. c_(i+1) is the immediate temporal successor of c(i),
            for every i ranging from 0 to len(expr) - 1.

      Otherwise False.

      A stricter version of _are_containerized_components(expr).'''

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
