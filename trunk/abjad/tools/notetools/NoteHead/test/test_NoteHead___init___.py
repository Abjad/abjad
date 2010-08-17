from abjad import *


def test_NoteHead___init____01( ):
   '''Init note head by number.'''

   t = notetools.NoteHead(None, 6)
   assert t.pitch == pitchtools.NamedPitch(6)


def test_NoteHead___init____02( ):
   '''Init note head by LilyPond-style pitch string.'''

   t = notetools.NoteHead(None, 'cs,,,')
   assert t.pitch == pitchtools.NamedPitch('cs,,,')


def test_NoteHead___init____03( ):
   '''Init note head by other note head instance.'''

   t = notetools.NoteHead(None, 6)
   new = notetools.NoteHead(None, t)

   assert t is not new
   assert t.pitch.number == 6
   assert new.pitch.number == 6
