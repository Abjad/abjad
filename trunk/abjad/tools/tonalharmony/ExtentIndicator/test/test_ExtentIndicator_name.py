from abjad import *


def test_ExtentIndicator_name_01( ):

   assert tonalharmony.ExtentIndicator(5).name == 'triad'
   assert tonalharmony.ExtentIndicator(7).name == 'seventh'
   assert tonalharmony.ExtentIndicator(9).name == 'ninth'
