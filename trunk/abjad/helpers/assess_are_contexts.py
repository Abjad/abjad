from abjad.context.context import _Context
import types

def assess_are_contexts(expr):
   '''Returns true if all the elements in expr are Contexts, 
   false otherwise.'''
   if not isinstance(expr, (list, types.GeneratorType)):
      raise TypeError('expr be list or a generator.')

   for element in expr:
      if not isinstance(element, _Context):
         return False
   return True
   
