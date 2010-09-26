from abjad.components._Component import _Component
import types


def all_are_components_in_same_parent(expr, klasses = (_Component, ), allow_orphans = True):
   '''True when expr is a Python list of Abjad components,
   and when all components have a parent and have the same parent.

   Otherwise False.
   '''

   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      raise TypeError('must be list of components: "%s".' % str(expr))

   if len(expr) == 0:
      return True 

   first = expr[0]
   if not isinstance(first, klasses):
      return False

   first_parent = first.parentage.parent
   if first_parent is None and not allow_orphans:
      return False

   for element in expr[1:]:
      if not isinstance(element, klasses):
         return False
      if element.parentage.parent is not first_parent:
         return False

   return True
