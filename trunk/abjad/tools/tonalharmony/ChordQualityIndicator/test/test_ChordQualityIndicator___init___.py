from abjad import *


def test_ChordQualityIndicator___init____01( ):
   '''Init root position triad.'''

   cqi = tonalharmony.ChordQualityIndicator('major', 'triad')
   assert str(cqi) == '<P1, M3, P5>'

   cqi = tonalharmony.ChordQualityIndicator('minor', 'triad')
   assert str(cqi) == '<P1, m3, P5>'

   cqi = tonalharmony.ChordQualityIndicator('diminished', 'triad')
   assert str(cqi) == '<P1, m3, dim5>'

   cqi = tonalharmony.ChordQualityIndicator('augmented', 'triad')
   assert str(cqi) == '<P1, M3, aug5>'

   
def test_ChordQualityIndicator___init____02( ):
   '''Init seventh and ninth.'''

   cqi = tonalharmony.ChordQualityIndicator('dominant', 7, 'root')
   assert str(cqi) == '<P1, M3, P5, m7>'

   cqi = tonalharmony.ChordQualityIndicator('dominant', 9, 'root')
   assert str(cqi) == '<P1, M3, P5, m7, M9>'


def test_ChordQualityIndicator___init____03( ):
   '''Init with quality string and integer cardinality indicator.'''

   cqi = tonalharmony.ChordQualityIndicator('dominant', 7)
   assert str(cqi) == '<P1, M3, P5, m7>'

   cqi = tonalharmony.ChordQualityIndicator('major', 7)
   assert str(cqi) == '<P1, M3, P5, M7>'

   cqi = tonalharmony.ChordQualityIndicator('diminished', 7)
   assert str(cqi) == '<P1, m3, dim5, dim7>'

   cqi = tonalharmony.ChordQualityIndicator('dominant', 9)
   assert str(cqi) == '<P1, M3, P5, m7, M9>'
