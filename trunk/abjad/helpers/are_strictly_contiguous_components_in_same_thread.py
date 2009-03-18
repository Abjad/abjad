from abjad.component.component import _Component


def _are_strictly_contiguous_components_in_same_thread(expr):
   '''True when expr is a Python list of Abjad components such that
         
         1. all components in list are strictly contiguous, and
         2. all components in list are in the same thread.

      Otherwise False.'''
   
   if isinstance(expr, list):
      if len(expr) == 0:
         return True
      first = expr[0]
      if isinstance(first, _Component):
         first_signature = first.parentage._containmentSignature
         prev = first
         for cur in expr[1:]:
            if not isinstance(cur, _Component):
               return False
            cur_signature = cur.parentage._containmentSignature
            if not cur_signature == first_signature:
               return False
            if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
               return False
            prev = cur
         return True
   return False
