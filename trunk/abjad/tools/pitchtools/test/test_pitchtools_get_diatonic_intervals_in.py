from abjad import *


def test_pitchtools_get_diatonic_intervals_in_01( ):

   staff = Staff(construct.scale(4))

   intervals = pitchtools.get_diatonic_intervals_in(staff)
   intervals = list(intervals)
   numbers = [interval.number for interval in intervals]
   numbers.sort( )

   assert numbers == [2, 2, 2, 3, 3, 4]
