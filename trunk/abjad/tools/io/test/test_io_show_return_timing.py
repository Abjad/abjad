from abjad import *


def test_io_show_return_timing_01( ):
   '''When return_timing is True, return Abjad format time as 
   an integer number of seconds and also return LilyPond render 
   time as integer number of seconds. Otherwise, return None.
   '''

   t = Staff(construct.run(4))

   ## we suppress the PDF here only while running py.test
   result = show(t, suppress_pdf = True)
   assert result is None

   ## we suppress the PDF here only while running py.test
   result = show(t, return_timing = True, suppress_pdf = True)
   assert isinstance(result, tuple)
   assert len(result) == 2
   assert isinstance(result[0], int)
   assert isinstance(result[1], int)
