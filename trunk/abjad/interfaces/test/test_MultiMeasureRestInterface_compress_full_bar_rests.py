from abjad import *


def test_MultiMeasureRestInterface_compress_full_bar_rests_01( ):

   staff = Staff([Note(0, (1, 4))])
   marktools.LilyPondCommandMark('compressFullBarRests')(staff[0])

   r'''
   \new Staff {
      \compressFullBarRests
      c'4
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\compressFullBarRests\n\tc'4\n}"


def test_MultiMeasureRestInterface_compress_full_bar_rests_02( ):

   staff = Staff([Note(0, (1, 4))])
   marktools.LilyPondCommandMark('expandFullBarRests')(staff[0])

   r'''
   \new Staff {
      \expandFullBarRests
      c'4
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\expandFullBarRests\n\tc'4\n}"   
