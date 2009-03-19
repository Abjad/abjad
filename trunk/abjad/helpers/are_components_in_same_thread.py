from abjad.component.component import _Component


#def _are_components_in_same_thread(expr, allow_orphans = True):
#   '''True when expr is a Python list of Abjad components such
#      that all components in list carry the same thread signature.
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
#   orphan_components = True
#   if not first.parentage.orphan:
#      orphan_components = False
#
#   same_thread = True
#
#   first_signature = first.parentage._threadSignature
#   for component in expr[1:]:
#      if not component.parentage.orphan:
#         orphan_components = False
#      if component.parentage._threadSignature != first_signature:
#         same_thread = False
#      if not allow_orphans and not same_thread:
#         return False
#      if allow_orphans and not orphan_components and not same_thread:
#         return False
#
#   return True
