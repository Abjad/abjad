from abjad import *
import py.test


def test__LeafDurationInterface___max___01( ):
   '''Leaf durations can go up to 'maxima...': duration < (16, 1).
   '''

   t = Note(1, 2)

   assert t.format == "cs'\\breve"
   t.duration.written = Duration(3)
   assert t.format == "cs'\\breve."
   t.duration.written = Duration(4)
   assert t.format == "cs'\\longa"
   t.duration.written = Duration(6)
   assert t.format == "cs'\\longa."
   t.duration.written = Duration(7)
   assert t.format == "cs'\\longa.."
   t.duration.written = Duration(8)
   assert t.format == "cs'\\maxima"
   t.duration.written = Duration(12)
   assert t.format == "cs'\\maxima."
   t.duration.written = Duration(14)
   assert t.format == "cs'\\maxima.."
   t.duration.written = Duration(15)
   assert t.format == "cs'\\maxima..."
   assert py.test.raises(AssignabilityError, 'Note(1, 16)')
