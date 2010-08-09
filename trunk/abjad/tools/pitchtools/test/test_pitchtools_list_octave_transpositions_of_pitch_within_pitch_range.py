from abjad import *


def test_pitchtools_list_octave_transpositions_of_pitch_within_pitch_range_01( ):
   '''List all octave transposition of pitches in range r.'''

   chord = Chord([0, 2, 4], (1, 4))
   pitch_range = pitchtools.PitchRange(0, 48)
   transpositions = pitchtools.list_octave_transpositions_of_pitch_within_pitch_range(chord, pitch_range)

   r"""
   [Chord(c' d' e', 4), Chord(c'' d'' e'', 4), Chord(c''' d''' e''', 4), Chord(c'''' d'''' e'''', 4)]
   """

   assert len(transpositions) == 4
   assert transpositions[0].signature == \
      ((('c', 4), ('d', 4), ('e', 4)), (1, 4))
   assert transpositions[1].signature == \
      ((('c', 5), ('d', 5), ('e', 5)), (1, 4))
   assert transpositions[2].signature == \
      ((('c', 6), ('d', 6), ('e', 6)), (1, 4))
   assert transpositions[3].signature == \
      ((('c', 7), ('d', 7), ('e', 7)), (1, 4))


def test_pitchtools_list_octave_transpositions_of_pitch_within_pitch_range_02( ):
   '''Works on pitch numbers.'''

   pitch_numbers = [0, 2, 4]
   pitch_range = pitchtools.PitchRange(0, 48)
   t = pitchtools.list_octave_transpositions_of_pitch_within_pitch_range(pitch_numbers, pitch_range)
   
   assert t == [[0, 2, 4], [12, 14, 16], [24, 26, 28], [36, 38, 40]]
