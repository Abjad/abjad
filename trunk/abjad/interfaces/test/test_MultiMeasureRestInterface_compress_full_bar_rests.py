from abjad import *


def test_MultiMeasureRestInterface_compress_full_bar_rests_01( ):

   staff = Staff([Note(0, (1, 4))])
   #staff[0].multi_measure_rest.compress_full_bar_rests = True
   staff[0].misc.compress_full_bar_rests = None

   r'''
   \new Staff {
      \compressFullBarRests
      c'4
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\compressFullBarRests\n\tc'4\n}"


def test_MultiMeasureRestInterface_compress_full_bar_rests_02( ):

   staff = Staff([Note(0, (1, 4))])
   #staff[0].multi_measure_rest.compress_full_bar_rests = False
   staff[0].misc.expand_full_bar_rests = None

   r'''
   \new Staff {
      \expandFullBarRests
      c'4
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\expandFullBarRests\n\tc'4\n}"   
