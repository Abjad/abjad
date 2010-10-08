from abjad import *


def test_pitchtools_list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers_01( ):

   staff = Staff(macros.scale(8))
   t = pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers(staff)

   assert t == [2, 2, 1, 2, 2, 2, 1]

   staff = Staff(macros.scale(8))
   t = pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers(staff, wrap = True)

   assert t == [2, 2, 1, 2, 2, 2, 1, -12]



def test_pitchtools_list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers_02( ):

   notes = macros.scale(8)
   notes.reverse( )
   t = pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers(notes)

   assert t == [-1, -2, -2, -2, -1, -2, -2]

   t = pitchtools.list_melodic_chromatic_interval_numbers_pairwise_between_ppitch_carriers(notes, wrap = True)

   assert t == [-1, -2, -2, -2, -1, -2, -2, 12]
