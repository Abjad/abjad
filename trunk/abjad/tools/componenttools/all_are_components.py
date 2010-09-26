from abjad.components._Component import _Component
import types


def all_are_components(expr, klasses = (_Component, )):
   '''True when expr is a Python list of Abjad components.

   Otherwise False.
   '''

   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      raise TypeError('must be a list of Abjad components: "%s".' % str(expr))

   for element in expr:
      if not isinstance(element, klasses):
         return False

   return True
