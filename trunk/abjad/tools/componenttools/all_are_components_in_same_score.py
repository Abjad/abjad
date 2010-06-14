from abjad.component import _Component
import types


def all_are_components_in_same_score(expr, klasses = (_Component, ), allow_orphans = True):
   '''True when expr is a Python list of Abjad components,
      and when all components have the same score root.
      Otherwise False.
   '''

   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      raise TypeError('Must be list of Abjad components.')
      
   if len(expr) == 0:
      return True 

   first = expr[0]
   if not isinstance(first, klasses):
      return False

   first_parent = first.parentage.parent
   first_score = first.parentage.root
   for element in expr[1:]:
      if not isinstance(element, klasses):
         return False
      if element.parentage.root is not first_score:
         if not (allow_orphans and element.parentage.orphan):
            return False

   return True
