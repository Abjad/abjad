from abjad import *


def test_pitchtools_PitchSet___init___01( ):
   '''Works with numbers.'''

   assert len(pitchtools.PitchSet([12, 14, 18, 19])) == 4


def test_pitchtools_PitchSet___init___02( ):
   '''Works with pitches.'''

   assert len(pitchtools.PitchSet([Pitch(x) for x in [12, 14, 18, 19]])) == 4
