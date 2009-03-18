from abjad.component.component import _Component


def _are_strictly_contiguous_components_in_same_score(
   expr, allow_orphans = True):
   '''True when expr is a Python list of Abjad components such that

         1. all components in list are strictly contiguous, and
         2. every component in list is in the same score.

      Otherwise False.'''

   if not isinstance(expr, list):
      raise TypeError('Must be list of Abjad components.')

   if len(expr) == 0:
      return True

   first = expr[0]
   if not isinstance(first, _Component):
      return False

   orphan_components = True   
   if not first.parentage.orphan:
      orphan_components = False

   same_score = True
   strictly_contiguous = True

   first_score = first.parentage.root
   prev = first
   for cur in expr[1:]:
      if not isinstance(cur, _Component):
         return False
      if not cur.parentage.orphan:
         orphan_components = False
      if not cur.parentage.root is first_score:
         #return False
         same_score = False
      if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
         #return False
         strictly_contiguous = False
      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
         (not same_score or not strictly_contiguous):
         return False
      prev = cur

   return True
