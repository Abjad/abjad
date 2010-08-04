from abjad import *


def test_NoteHead___init____01( ):
   '''Init note head by number.'''

   t = NoteHead(None, 6)
   assert t.pitch == NamedPitch(6)


def test_NoteHead___init____02( ):
   '''Init note head by LilyPond-style pitch string.'''

   t = NoteHead(None, 'cs,,,')
   assert t.pitch == NamedPitch('cs,,,')


def test_NoteHead___init____03( ):
   '''Init note head by other note head instance.'''

   t = NoteHead(None, 6)
   new = NoteHead(None, t)

   assert t is not new
   assert t.pitch.number == 6
   assert new.pitch.number == 6
