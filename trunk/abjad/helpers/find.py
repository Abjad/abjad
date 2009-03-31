from abjad.component.component import _Component
from abjad.helpers.iterate import iterate


def find(expr, name = None, klass = None, context = None):
   '''Iterate expr. 
      Find and return a Python list of all components in expr, such that:

         * component.name == name
         * isinstance(component, klass)
         * component.context == context

      Do not run tests where keyword is None.

      For shallow traversal of container for numeric indices,
      use Container.__getitem__(i) instead.'''

   result = [ ]

   for component in iterate(expr, _Component):
      if name is None or component.name == name:
         if klass is None or isinstance(component, klass):
            if context is None or \
               getattr(component, 'context', None) == context:
               result.append(component)

   return result
