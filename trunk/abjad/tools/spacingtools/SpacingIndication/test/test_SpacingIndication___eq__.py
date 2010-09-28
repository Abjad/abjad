from abjad import *


def test_SpacingIndication___eq___01( ):
   '''Spacing indications compare equal when 
      normalized spacing durations compare equal.'''

   tempo_indication = marktools.TempoMark(Fraction(1, 8), 38)
   p = spacingtools.SpacingIndication(tempo_indication, Fraction(1, 68))
   
   tempo_indication = marktools.TempoMark(Fraction(1, 4), 76)
   q = spacingtools.SpacingIndication(tempo_indication, Fraction(1, 68))

   assert p == q
   

def test_SpacingIndication___eq___02( ):
   '''Spacing indications compare not equal when 
      normalized spacing durations compare not equal.'''

   tempo_indication = marktools.TempoMark(Fraction(1, 8), 38)
   p = spacingtools.SpacingIndication(tempo_indication, Fraction(1, 68))
   
   tempo_indication = marktools.TempoMark(Fraction(1, 8), 38)
   q = spacingtools.SpacingIndication(tempo_indication, Fraction(1, 78))

   assert p != q
