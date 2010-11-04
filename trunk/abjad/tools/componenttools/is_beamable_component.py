def is_beamable_component(expr):
   '''.. versionadded:: 1.1.2

   True when `expr` is a beamable component. Otherwise false::

      abjad> componenttools.is_beamable_component(Note(13, (1, 16)))
      True

   Return boolean.
   '''
   from abjad.components._Leaf import _Leaf
   from abjad.components import Chord
   from abjad.components import Note
   from abjad.tools import durtools

   #if isinstance(expr, _Leaf):
   if isinstance(expr, (Note, Chord)):
      if 0 < durtools.rational_to_flag_count(expr.duration.written):
         return True
   return False
