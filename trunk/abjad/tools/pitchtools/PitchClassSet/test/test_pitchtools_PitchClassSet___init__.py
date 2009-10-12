from abjad import *


def test_pitchtools_PitchClassSet___init___01( ):
   '''Works with numbers.'''

   assert len(pitchtools.PitchClassSet([0, 2, 6, 7])) == 4


def test_pitchtools_PitchClassSet___init___02( ):
   '''Works with pitch classes.'''

   assert len(pitchtools.PitchClassSet(
      [pitchtools.PitchClass(x) for x in [0, 2, 6, 7]])) == 4
