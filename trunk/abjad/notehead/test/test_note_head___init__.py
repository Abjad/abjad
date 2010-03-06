from abjad import *


def test_note_head___init___01( ):
   '''Init note head by number.'''

   t = NoteHead(None, 6)
   assert t.pitch == Pitch(6)


def test_note_head___init___02( ):
   '''Init note head by LilyPond-style pitch string.'''

   t = NoteHead(None, 'cs,,,')
   assert t.pitch == Pitch('cs,,,')


def test_note_head___init___03( ):
   '''Init note head by other note head instance.'''

   t = NoteHead(None, 6)
   new = NoteHead(None, t)

   assert t is not new
   assert t.pitch.number == 6
   assert new.pitch.number == 6
