from abjad.component import _Component
import types


def all_are_components(expr, klasses = (_Component, )):
   '''True when expr is a Python list of Abjad components.
      otherwise False.
   '''

   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      raise TypeError('expr must be a list of Abjad components.')

   for element in expr:
      if not isinstance(element, klasses):
         return False

   return True
