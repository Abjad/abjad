from abjad.component.component import _Component


#def _are_strictly_contiguous_components_in_same_parent(
#   expr, allow_orphans = True):
#   '''True when expr is a Python list of Abjad components such that
#
#         1. all components in list are strictly contiguous, and
#         2. every component in list has the same parent.
#
#      Otherwise False.'''
#
#   if not isinstance(expr, list):
#      raise TypeError('Must be list of Abjad components.')
#
#   if len(expr) == 0:
#      return True
#
#   first = expr[0]
#   if not isinstance(first, _Component):
#      return False
#
#   first_parent = first.parentage.parent
#   if first_parent is None:
#      if allow_orphans:
#         orphan_components = True
#      else:
#         return False
#   
#   same_parent = True
#   strictly_contiguous = True
#
#   prev = first
#   for cur in expr[1:]:
#      if not isinstance(cur, _Component):
#         return False
#      if not cur.parentage.orphan:
#         orphan_components = False
#      if not cur.parentage.parent is first_parent:
#         #return False
#         same_parent = False
#      if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
#         #return False
#         strictly_contiguous = False
#      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
#         (not same_parent or not strictly_contiguous):
#         return False
#      prev = cur
#
#   return True
