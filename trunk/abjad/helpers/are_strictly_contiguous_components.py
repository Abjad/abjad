from abjad.component.component import _Component


#def _are_strictly_contiguous_components(expr, allow_orphans = True):
#   '''True expr is a Python list of strictly contiguous components.
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
#   orphan_components = True
#   if not first.parentage.orphan:
#      orphan_components = False
#
#   strictly_contiguous = True
#
#   prev = first
#   for cur in expr[1:]:
#      if not isinstance(cur, _Component):
#         return False
#      if not cur.parentage.orphan:
#         orphan_components = False
#      if not prev._navigator._isImmediateTemporalSuccessorOf(cur):
#         strictly_contiguous = False
#      if (not allow_orphans or (allow_orphans and not orphan_components)) and \
#         not strictly_contiguous:
#         return False
#      prev = cur
#
#   return True
