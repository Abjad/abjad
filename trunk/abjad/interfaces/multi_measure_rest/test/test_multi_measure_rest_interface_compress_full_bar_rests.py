from abjad import *


def test_multi_measure_rest_interface_compress_full_bar_rests_01( ):

   staff = Staff([Note(0, (1, 4))])
   staff[0].multi_measure_rest.compress_full_bar_rests = True

   r'''
   \new Staff {
      \compressFullBarRests
      c'4
   }
   '''

   assert staff.format == "\\new Staff {\n\t\\compressFullBarRests\n\tc'4\n}"
