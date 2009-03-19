from abjad.component.component import _Component


#def _are_components_in_same_parent(expr, allow_orphans = True):
#   '''True when expr is a Python list of Abjad components,
#      and when all components have a parent and have the same parent.
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
#   if first_parent is None and not allow_orphans:
#      return False
#
#   for element in expr[1:]:
#      if not isinstance(element, _Component):
#         return False
#      if element.parentage.parent is not first_parent:
#         return False
#
#   return True
