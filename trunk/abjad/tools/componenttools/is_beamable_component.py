def is_beamable_component(expr):
   '''.. versionadded:: 1.1.1

   True when `expr` is a beamable component. Otherwise false::

      abjad> componenttools.is_beamable_component(Note(13, (1, 16)))
      True

   Return boolean.
   '''
   from abjad.tools.leaftools._Leaf import _Leaf
   from abjad.tools.chordtools.Chord import Chord
   from abjad.tools.notetools.Note import Note
   from abjad.tools import durtools

   #if isinstance(expr, _Leaf):
   if isinstance(expr, (Note, Chord)):
      if 0 < durtools.rational_to_flag_count(expr.duration.written):
         return True
   return False
