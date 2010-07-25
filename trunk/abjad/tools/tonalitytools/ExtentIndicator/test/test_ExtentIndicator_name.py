from abjad import *


def test_ExtentIndicator_name_01( ):

   assert tonalitytools.ExtentIndicator(5).name == 'triad'
   assert tonalitytools.ExtentIndicator(7).name == 'seventh'
   assert tonalitytools.ExtentIndicator(9).name == 'ninth'
