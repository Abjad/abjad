from abjad import *


def test_NoteHead___eq___01( ):
   '''Noteheads compare equal when note_head pitches compare equal.'''

   assert notetools.NoteHead(None, 14) == notetools.NoteHead(None, 14)
   assert notetools.NoteHead(None, pitchtools.NamedPitch('df', 5)) == \
      notetools.NoteHead(None, pitchtools.NamedPitch('df', 5))


def test_NoteHead___eq___02( ):
   '''NoteHeads compare unequal when note_head pitches compare unequal.'''

   assert not notetools.NoteHead(None, 14) == notetools.NoteHead(None, 15)
   assert not notetools.NoteHead(None, pitchtools.NamedPitch('cs', 5)) == \
      notetools.NoteHead(None, pitchtools.NamedPitch('df', 5))
