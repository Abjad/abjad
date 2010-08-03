from abjad._Leaf import _Leaf
from abjad.Rational import Rational


def change_written_duration_and_preserve_preprolated_duration(leaf, written_duration):
   '''Change `leaf` written duration to `written_duration` and 
   preserve `leaf` preprolated duration::

      abjad> note = Note(0, (1, 4))
      abjad> note.duration.written 
      Rational(1, 4)
      abjad> note.duration.preprolated 
      Rational(1, 4)
      
   ::
      
      abjad> leaftools.change_written_duration_and_preserve_preprolated_duration(note, Rational(3, 16)) 
      Note(c', 8. * 4/3)
      
   ::
      
      abjad> note.duration.written 
      Rational(3, 16)
      abjad> note.duration.preprolated 
      Rational(1, 4)

   Add LilyPond multiplier where necessary.

   Return `leaf`.
   
   .. versionchanged:: 1.1.2
      Renamed from ``leaftools.duration_rewrite( )``.
   '''

   ## check leaf type
   if not isinstance(leaf, _Leaf):
      raise TypeError('must be leaf: %s' % leaf)

   ## check written duration type
   written_duration = Rational(written_duration)

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
