from abjad import *


def test_NoteHead___eq___01( ):
   '''Note heads compare equal when note head pitches compare equal.
   '''

   assert notetools.NoteHead(14) == notetools.NoteHead(14)
   assert notetools.NoteHead(pitchtools.NamedPitch('df', 5)) == \
      notetools.NoteHead(pitchtools.NamedPitch('df', 5))


def test_NoteHead___eq___02( ):
   '''Note heads compare unequal when note head pitches compare unequal.
   '''

   assert not notetools.NoteHead(14) == notetools.NoteHead(15)
   assert not notetools.NoteHead(pitchtools.NamedPitch('cs', 5)) == \
      notetools.NoteHead(pitchtools.NamedPitch('df', 5))
