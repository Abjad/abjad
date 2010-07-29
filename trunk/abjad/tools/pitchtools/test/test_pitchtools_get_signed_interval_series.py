from abjad import *


def test_pitchtools_get_signed_interval_series_01( ):

   staff = Staff(macros.scale(8))
   t = pitchtools.get_signed_interval_series(staff)

   assert t == [2, 2, 1, 2, 2, 2, 1]

   staff = Staff(macros.scale(8))
   t = pitchtools.get_signed_interval_series(staff, wrap = True)

   assert t == [2, 2, 1, 2, 2, 2, 1, -12]



def test_pitchtools_get_signed_interval_series_02( ):

   notes = macros.scale(8)
   notes.reverse( )
   t = pitchtools.get_signed_interval_series(notes)

   assert t == [-1, -2, -2, -2, -1, -2, -2]

   t = pitchtools.get_signed_interval_series(notes, wrap = True)

   assert t == [-1, -2, -2, -2, -1, -2, -2, 12]
