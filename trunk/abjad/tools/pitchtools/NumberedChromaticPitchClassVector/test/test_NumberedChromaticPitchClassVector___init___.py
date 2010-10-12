from abjad import *


def test_NumberedChromaticPitchClassVector___init____01( ):
   
   pcv = pitchtools.NumberedChromaticPitchClassVector([5, 6, 7, 8, 10, 11])
   assert pcv.numbers == [5, 6, 7, 8, 10, 11]


def test_NumberedChromaticPitchClassVector___init____02( ):
   
   pcv = pitchtools.NumberedChromaticPitchClassVector([1.5, 5, 6, 7, 8, 10, 11])
   assert pcv.numbers == [1.5, 5, 6, 7, 8, 10, 11]
