from abjad import *


def test_pitchtools_PCSet___init___01( ):
   '''Works with numbers.'''

   assert len(pitchtools.PCSet([0, 2, 6, 7])) == 4


def test_pitchtools_PCSet___init___02( ):
   '''Works with PCs.'''

   assert len(pitchtools.PCSet([pitchtools.PC(x) for x in [0, 2, 6, 7]])) == 4
