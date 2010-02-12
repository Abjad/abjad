from abjad import *


def test_ChordQualityIndicator___init___01( ):
   '''Init with triad quality string alone.'''

   cqi = tonalharmony.ChordQualityIndicator('major')
   assert str(cqi) == '{P1, M3, P5}'

   cqi = tonalharmony.ChordQualityIndicator('minor')
   assert str(cqi) == '{P1, m3, P5}'

   cqi = tonalharmony.ChordQualityIndicator('diminished')
   assert str(cqi) == '{P1, m3, dim5}'

   cqi = tonalharmony.ChordQualityIndicator('augmented')
   assert str(cqi) == '{P1, M3, aug5}'

   
def test_ChordQualityIndicator___init___02( ):
   '''Init with integer cardinality indicator alone.'''

   cqi = tonalharmony.ChordQualityIndicator(7)
   assert str(cqi) == '{P1, M3, P5, m7}'

   cqi = tonalharmony.ChordQualityIndicator(9)
   assert str(cqi) == '{P1, M3, P5, m7, M9}'


def test_ChordQualityIndicator___init___03( ):
   '''Init with quality string and integer cardinality indicator.'''

   cqi = tonalharmony.ChordQualityIndicator('dominant', 7)
   assert str(cqi) == '{P1, M3, P5, m7}'

   cqi = tonalharmony.ChordQualityIndicator('major', 7)
   assert str(cqi) == '{P1, M3, P5, M7}'

   cqi = tonalharmony.ChordQualityIndicator('diminished', 7)
   assert str(cqi) == '{P1, m3, dim5, dim7}'

   cqi = tonalharmony.ChordQualityIndicator('dominant', 9)
   assert str(cqi) == '{P1, M3, P5, m7, M9}'
