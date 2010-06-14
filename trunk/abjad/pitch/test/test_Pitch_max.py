from abjad import *


def test_Pitch_max_01( ):
   '''Built-in max( ) works when __gt__ is defined.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   pitches = [note.pitch for note in t]
   max_pitch = max(pitches)

   assert max_pitch == Pitch('f', 4)
