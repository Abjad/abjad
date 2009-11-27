from abjad import *


def test_pitchtools_get_chromatic_intervals_in_01( ):

   staff = Staff(construct.scale(4))

   intervals = pitchtools.get_chromatic_intervals_in(staff)
   intervals = sorted(list(intervals))
   interval_numbers = [i.interval_number for i in intervals]

   assert interval_numbers == [1, 2, 2, 3, 4, 5]
