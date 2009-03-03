from abjad.component.component import _Component


def _are_components(expr):
   '''True when expr is a Python list of Abjad components,
      otherwise False.'''

   if isinstance(expr, list):
      for element in expr:
         if not isinstance(element, _Component):
            return False
      return True

   return False
