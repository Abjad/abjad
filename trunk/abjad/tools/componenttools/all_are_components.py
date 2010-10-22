from abjad.components._Component import _Component
import types


def all_are_components(expr, klasses = None):
   '''True when elements in `expr` are all components. Otherwise false::

      abjad> notes = notetools.make_notes([12, 14, 16], [(1, 8)])
      abjad> componenttools.all_are_components(notes) 
      True

   True when elements in `expr` are all `klasses`. Otherwise false::

      abjad> notes = notetools.make_notes([12, 14, 16], [(1, 8)])
      abjad> componenttools.all_are_components(notes, klasses = (Note, )) 
      True

   Return boolean.
   '''

   if not isinstance(expr, (list, tuple, types.GeneratorType)):
      #raise TypeError('must be a list of Abjad components: "%s".' % str(expr))
      return False

   if klasses is None:
      klasses = _Component

   for element in expr:
      if not isinstance(element, klasses):
         return False

   return True
