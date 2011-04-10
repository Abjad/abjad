from abjad import *
import py.test


def test__LeafDurationInterface___max___01( ):
   '''Leaf durations can go up to 'maxima...': duration < (16, 1).
   '''

   t = Note(1, 2)

   assert t.format == "cs'\\breve"
   t.duration.written = Fraction(3)
   assert t.format == "cs'\\breve."
   t.duration.written = Fraction(4)
   assert t.format == "cs'\\longa"
   t.duration.written = Fraction(6)
   assert t.format == "cs'\\longa."
   t.duration.written = Fraction(7)
   assert t.format == "cs'\\longa.."
   t.duration.written = Fraction(8)
   assert t.format == "cs'\\maxima"
   t.duration.written = Fraction(12)
   assert t.format == "cs'\\maxima."
   t.duration.written = Fraction(14)
   assert t.format == "cs'\\maxima.."
   t.duration.written = Fraction(15)
   assert t.format == "cs'\\maxima..."
   assert py.test.raises(AssignabilityError, 'Note(1, 16)')
