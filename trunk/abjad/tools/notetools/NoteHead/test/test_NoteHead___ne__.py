from abjad import *


def test_NoteHead___ne___01( ):
   '''Noteheads compare equal when note_head pitches compare equal.'''

   assert not notetools.NoteHead(None, 14) != notetools.NoteHead(None, 14)
   assert not notetools.NoteHead(None, pitchtools.NamedPitch('df', 5)) != \
      notetools.NoteHead(None, pitchtools.NamedPitch('df', 5))


def test_NoteHead___ne___02( ):
   '''NoteHeads compare unequal when note_head pitches compare unequal.'''

   assert notetools.NoteHead(None, 14) != notetools.NoteHead(None, 15)
   assert notetools.NoteHead(None, pitchtools.NamedPitch('cs', 5)) != \
      notetools.NoteHead(None, pitchtools.NamedPitch('df', 5))
