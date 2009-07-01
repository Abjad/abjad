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


def test_notehead_pitch_04( ):
   '''Set NoteHead pitch from another note or notehead.
   Make sure this does not cause reference problems.'''

   n1 = Note(12, (1, 4))
   n2 = Note(14, (1, 4))
   n1.pitch = n2.pitch

   assert n1.pitch == Pitch(14)
   assert n2.pitch == Pitch(14)
   assert n1.pitch is not n2.pitch
