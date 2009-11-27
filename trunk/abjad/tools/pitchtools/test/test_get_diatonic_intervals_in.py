from abjad import *


def test_pitchtools_get_diatonic_intervals_in_01( ):

   staff = Staff(construct.scale(4))

   intervals = pitchtools.get_diatonic_intervals_in(staff)
   intervals = list(intervals)
   interval_numbers = [interval.interval_number for interval in intervals]
   interval_numbers.sort( )

   assert interval_numbers == [2, 2, 2, 3, 3, 4]
