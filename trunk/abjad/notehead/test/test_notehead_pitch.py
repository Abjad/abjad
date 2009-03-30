from abjad import *
import py.test


def test_notehead_pitch_01( ):
   '''Set NoteHead pitch with integer.'''

   t = Note(13, (1, 4))
   t.notehead.pitch = 14

   "NoteHead(d'')"
   assert t.notehead.format == "d''"
   assert t.notehead.pitch.number == 14


def test_notehead_pitch_02( ):
   '''Set NoteHead pitch with Abjad Pitch object.'''

   t = Note(13, (1, 4))
   t.notehead.pitch = Pitch(14)

   "NoteHead(d'')"
   assert t.notehead.format == "d''"
   assert t.notehead.pitch.number == 14


def test_notehead_pitch_03( ):
   '''Set NoteHead pitch to None.'''

   t = Note(13, (1, 4))
   t.notehead.pitch = None

   "NoteHead( )"
   assert t.notehead.pitch == None
   assert py.test.raises(AssertionError, 't.notehead.format')
