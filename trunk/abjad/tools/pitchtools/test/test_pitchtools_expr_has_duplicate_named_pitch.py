from abjad import *


def test_pitchtools_expr_has_duplicate_named_pitch_01( ):
   '''Works with chords.'''

   assert pitchtools.expr_has_duplicate_named_pitch(Chord([13, 13, 14], (1, 4)))
   assert not pitchtools.expr_has_duplicate_named_pitch(Chord([13, 14], (1, 4)))
   assert not pitchtools.expr_has_duplicate_named_pitch(Chord([ ], (1, 4)))


def test_pitchtools_expr_has_duplicate_named_pitch_02( ):
   '''Works with notes, rests and skips.'''

   assert not pitchtools.expr_has_duplicate_named_pitch(Note(13, (1, 4)))
   assert not pitchtools.expr_has_duplicate_named_pitch(Rest((1, 4)))
   assert not pitchtools.expr_has_duplicate_named_pitch(Skip((1, 4)))


def test_pitchtools_expr_has_duplicate_named_pitch_03( ):
   '''Works with containers.'''

   staff = Staff(notetools.make_repeated_notes(4))
   assert pitchtools.expr_has_duplicate_named_pitch(staff)

   staff = Staff(macros.scale(4))
   assert not pitchtools.expr_has_duplicate_named_pitch(staff)
