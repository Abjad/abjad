from abjad import *


def test_PitchClassVector___init____01( ):
   
   pcv = pitchtools.PitchClassVector([5, 6, 7, 8, 10, 11])
   assert pcv.numbers == [5, 6, 7, 8, 10, 11]


def test_PitchClassVector___init____02( ):
   
   pcv = pitchtools.PitchClassVector([1.5, 5, 6, 7, 8, 10, 11])
   assert pcv.numbers == [1.5, 5, 6, 7, 8, 10, 11]
