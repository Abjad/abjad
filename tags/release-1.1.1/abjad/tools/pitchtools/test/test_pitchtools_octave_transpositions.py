from abjad import *


def test_pitchtools_octave_transpositions_01( ):
   '''List all octave transposition of pitches in range r.'''

   pitches = [0, 2, 4]
   t = pitchtools.octave_transpositions(pitches, [0, 48])

   assert t == [[0, 2, 4], [12, 14, 16], [24, 26, 28], [36, 38, 40]]
