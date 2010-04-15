from abjad import *


def test_ScaleDegree_roman_numeral_string_01( ):

   assert tonalharmony.ScaleDegree(1).roman_numeral_string == 'I'
   assert tonalharmony.ScaleDegree(2).roman_numeral_string == 'II'
   assert tonalharmony.ScaleDegree(3).roman_numeral_string == 'III'
   assert tonalharmony.ScaleDegree(4).roman_numeral_string == 'IV'
   assert tonalharmony.ScaleDegree(5).roman_numeral_string == 'V'
   assert tonalharmony.ScaleDegree(6).roman_numeral_string == 'VI'
   assert tonalharmony.ScaleDegree(7).roman_numeral_string == 'VII'
