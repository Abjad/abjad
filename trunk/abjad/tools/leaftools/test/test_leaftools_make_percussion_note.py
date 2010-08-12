from abjad import *

def test_leaftools_make_percussion_note_01( ):
   '''tied total_duration < max_note_duration.'''

   t = leaftools.make_percussion_note(1, (5, 64), (1, 1))

   assert len(t) == 2
   assert t[0].pitch.number == 1
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert t[0].duration.written == Rational(1, 16)
   assert t[1].duration.written == Rational(1, 64)
   assert not t[0].tie.spanned
   assert not t[1].tie.spanned


def test_leaftools_make_percussion_note_02( ):
   '''max_note_duration < tied total_duration.'''

   t = leaftools.make_percussion_note(1, (5, 64), (1, 64))

   assert len(t) == 2
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert t[0].duration.written == Rational(1, 64)
   assert t[1].duration.written == Rational(1, 16)
   assert not t[0].tie.spanned
   assert not t[1].tie.spanned


def test_leaftools_make_percussion_note_03( ):
   '''non-tied total_duration < max_note_duration.'''

   t = leaftools.make_percussion_note(1, (3, 64), (1, 1))

   assert len(t) == 1
   assert isinstance(t[0], Note)
   assert t[0].duration.written == Rational(3, 64)


def test_leaftools_make_percussion_note_04( ):
   '''max_note_duration < non-tied total_duration.'''

   t = leaftools.make_percussion_note(1, (3, 64), (1, 64))

   assert len(t) == 2
   assert isinstance(t[0], Note)
   assert isinstance(t[1], Rest)
   assert t[0].duration.written == Rational(1, 64)
   assert t[1].duration.written == Rational(1, 32)
   assert not t[0].tie.spanned
   assert not t[1].tie.spanned

