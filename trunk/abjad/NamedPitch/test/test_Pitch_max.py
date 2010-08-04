from abjad import *


def test_Pitch_max_01( ):
   '''Built-in max( ) works when __gt__ is defined.'''

   t = Staff(macros.scale(4))
   pitches = [note.pitch for note in t]
   max_pitch = max(pitches)

   assert max_pitch == Pitch('f', 4)
