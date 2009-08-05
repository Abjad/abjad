from abjad import *


def test_notehead_ne_01( ):
   '''Noteheads compare equal when notehead pitches compare equal.'''

   assert not NoteHead(None, 14) != NoteHead(None, 14)
   assert not NoteHead(None, Pitch('df', 5)) != NoteHead(None, Pitch('df', 5))


def test_notehead_ne_02( ):
   '''NoteHeads compare unequal when notehead pitches compare unequal.'''

   assert NoteHead(None, 14) != NoteHead(None, 15)
   assert NoteHead(None, Pitch('cs', 5)) != NoteHead(None, Pitch('df', 5))
