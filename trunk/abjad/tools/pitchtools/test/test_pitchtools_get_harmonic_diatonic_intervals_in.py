from abjad import *


def test_pitchtools_get_harmonic_diatonic_intervals_in_01( ):

   staff = Staff(macros.scale(4))

   intervals = pitchtools.get_harmonic_diatonic_intervals_in(staff)
   intervals = list(intervals)
   numbers = [hdi.number for hdi in intervals]
   numbers.sort( )

   assert numbers == [2, 2, 2, 3, 3, 4]
