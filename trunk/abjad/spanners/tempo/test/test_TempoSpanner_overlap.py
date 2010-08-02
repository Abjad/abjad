from abjad import *


def test_tempo_spanner_overlap_01( ):
   '''Overlapping tempo spanners are not well formed.'''

   t = Staff(macros.scale(4))
   TempoSpanner(t[:])
   TempoSpanner(t[:])

   assert not componenttools.is_well_formed_component(t)
