from abjad import *


def test_pitchtools_send_pitch_number_to_octave_01( ):
   '''Send pitch number to octave.'''

   mapping = [((-39, -13), 0), ((-12, 23), 12), ((24, 48), 24)]
   pitch_numbers = [-30, -18, -6, 6, 18, 30, 42]

   t = [ ]
   for pitch_number in pitch_numbers:
      t.append(pitchtools.send_pitch_number_to_octave(pitch_number, mapping))

   assert t == [6, 6, 18, 18, 18, 30, 30]


def test_pitchtools_send_pitch_number_to_octave_02( ):
   '''Send pitch number to octave.'''

   mapping = [((-39, -1), 0), ((0, 48), 6)]
   pitch_numbers = [-30, -18, -6, 6, 18, 30, 42]

   t = [ ]
   for pitch_number in pitch_numbers:
      t.append(pitchtools.send_pitch_number_to_octave(pitch_number, mapping))

   assert t == [6, 6, 6, 6, 6, 6, 6]


def test_pitchtools_send_pitch_number_to_octave_03( ):
   '''Send pitch number to octave.'''

   mapping = [((-39, -1), 0), ((0, 48), 6)]
   pitch_numbers = [-34, -22, -10, 2, 14, 26, 38]

   t = [ ]
   for pitch_number in pitch_numbers:
      t.append(pitchtools.send_pitch_number_to_octave(pitch_number, mapping))

   assert t == [2, 2, 2, 14, 14, 14, 14]
