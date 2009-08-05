from abjad import *


def test_notehead_eq_01( ):
   '''Noteheads compare equal when notehead pitches compare equal.'''

   assert NoteHead(None, 14) == NoteHead(None, 14)
   assert NoteHead(None, Pitch('df', 5)) == NoteHead(None, Pitch('df', 5))


def test_notehead_eq_02( ):
   '''NoteHeads compare unequal when notehead pitches compare unequal.'''

   assert not NoteHead(None, 14) == NoteHead(None, 15)
   assert not NoteHead(None, Pitch('cs', 5)) == NoteHead(None, Pitch('df', 5))
