from abjad import *
import py.test


def test_leaf_duration_interface_maximum_01( ):
   '''Leaf durations can go up to 'maxima...': duration < (16, 1) '''
   t = Note(1, 2)
   assert t.format == "cs'\\breve"
   t.duration.written = Rational(3)
   assert t.format == "cs'\\breve."
   t.duration.written = Rational(4)
   assert t.format == "cs'\\longa"
   t.duration.written = Rational(6)
   assert t.format == "cs'\\longa."
   t.duration.written = Rational(7)
   assert t.format == "cs'\\longa.."
   t.duration.written = Rational(8)
   assert t.format == "cs'\\maxima"
   t.duration.written = Rational(12)
   assert t.format == "cs'\\maxima."
   t.duration.written = Rational(14)
   assert t.format == "cs'\\maxima.."
   t.duration.written = Rational(15)
   assert t.format == "cs'\\maxima..."
   #assert py.test.raises(ValueError, 'Note(1, 16)')
   assert py.test.raises(AssignabilityError, 'Note(1, 16)')
