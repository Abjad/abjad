from abjad.components._Leaf import _Leaf
from abjad.tools import durtools


def change_written_leaf_duration_and_preserve_preprolated_leaf_duration(leaf, written_duration):
   '''.. versionadded:: 1.1.1

   Change `leaf` written duration to `written_duration` and preserve preprolated `leaf` duration::

      abjad> note = Note(0, (1, 4))
      abjad> note.duration.written 
      Duration(1, 4)
      abjad> note.duration.preprolated 
      Duration(1, 4)
      
   ::
      
      abjad> leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration(note, Duration(3, 16)) 
      Note("c'8. * 4/3")
      
   ::
      
      abjad> note.duration.written 
      Duration(3, 16)
      abjad> note.duration.preprolated 
      Duration(1, 4)

   Add LilyPond multiplier where necessary.

   Return `leaf`.
   
   .. versionchanged:: 1.1.2
      Renamed from ``leaftools.duration_rewrite( )``.
      ``leaftools.change_written_leaf_duration_and_preserve_preprolated_leaf_duration( )``.
   '''

   ## check leaf type
   if not isinstance(leaf, _Leaf):
      raise TypeError('must be leaf: %s' % leaf)

   ## check written duration type
   written_duration = durtools.Duration(written_duration)

   ## change leaf written duration
   previous = leaf.duration.multiplied
   leaf.duration.written = written_duration

   ## change leaf multiplier if required
   leaf.duration.multiplier = None
   multiplier = previous / leaf.duration.written
   if multiplier != 1:
      leaf.duration.multiplier = multiplier

   ## return leaf
   return leaf
