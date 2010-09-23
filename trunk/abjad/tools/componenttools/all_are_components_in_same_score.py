from abjad.components._Component import _Component
from abjad.tools.componenttools.component_is_orphan import component_is_orphan
from abjad.tools.componenttools.component_to_score_root import component_to_score_root
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

   first_parent = first._parentage.parent
   first_score = component_to_score_root(first)
   for element in expr[1:]:
      if not isinstance(element, klasses):
         return False
      if component_to_score_root(element) is not first_score:
         if not (allow_orphans and component_is_orphan(element)):
            return False

   return True
