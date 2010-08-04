from abjad import *


def test_NoteHead___eq___01( ):
   '''Noteheads compare equal when note_head pitches compare equal.'''

   assert NoteHead(None, 14) == NoteHead(None, 14)
   assert NoteHead(None, NamedPitch('df', 5)) == NoteHead(None, NamedPitch('df', 5))


def test_NoteHead___eq___02( ):
   '''NoteHeads compare unequal when note_head pitches compare unequal.'''

   assert not NoteHead(None, 14) == NoteHead(None, 15)
   assert not NoteHead(None, NamedPitch('cs', 5)) == NoteHead(None, NamedPitch('df', 5))
