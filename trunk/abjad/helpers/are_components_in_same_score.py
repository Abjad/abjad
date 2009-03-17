from abjad.component.component import _Component


def _are_components_in_same_score(expr):
   '''True when expr is a Python list of Abjad components,
      and when all components have the same score root.
      Otherwise False.'''

   if isinstance(expr, list):
      if len(expr) == 0:
         return True 
      first = expr[0]
      first_score = first.parentage.root
      for element in expr[1:]:
         if not isinstance(element, _Component):
            return False
         if element.parentage.root is not first_score:
            return False
      return True
   return False
