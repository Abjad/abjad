from abjad import *


def test_ScaleDegree_title_string_01( ):

   assert tonalharmony.ScaleDegree(1).title_string == 'One'
   assert tonalharmony.ScaleDegree(2).title_string == 'Two'
   assert tonalharmony.ScaleDegree(3).title_string == 'Three'
   assert tonalharmony.ScaleDegree(4).title_string == 'Four'
   assert tonalharmony.ScaleDegree(5).title_string == 'Five'
   assert tonalharmony.ScaleDegree(6).title_string == 'Six'
   assert tonalharmony.ScaleDegree(7).title_string == 'Seven'


def test_ScaleDegree_title_string_02( ):

   assert tonalharmony.ScaleDegree('sharp', 4).title_string == 'SharpFour'
   assert tonalharmony.ScaleDegree('flat', 6).title_string == 'FlatSix'
