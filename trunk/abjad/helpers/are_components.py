from abjad.component.component import _Component


def _are_components(expr):
   '''True when expr is a Python list of Abjad components.
      otherwise False.'''

   if not isinstance(expr, list):
      raise TypeError('expr must be a list of Abjad components.')

   for element in expr:
      if not isinstance(element, _Component):
         return False

   return True
