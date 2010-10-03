from abjad import *


def test_NoteHead___ne___01( ):
   '''Note heads compare equal when note head pitches compare equal.
   '''

   assert not notetools.NoteHead(14) != notetools.NoteHead(14)
   assert not notetools.NoteHead(pitchtools.NamedPitch('df', 5)) != \
      notetools.NoteHead(pitchtools.NamedPitch('df', 5))


def test_NoteHead___ne___02( ):
   '''Note heads compare unequal when note head pitches compare unequal.
   '''

   assert notetools.NoteHead(14) != notetools.NoteHead(15)
   assert notetools.NoteHead(pitchtools.NamedPitch('cs', 5)) != \
      notetools.NoteHead(pitchtools.NamedPitch('df', 5))
