from abjad import *


def test_TempoSpanner_overlap_01( ):
   '''Overlapping tempo spanners are not well formed.'''

   t = Staff(macros.scale(4))
   spannertools.TempoSpanner(t[:])
   spannertools.TempoSpanner(t[:])

   assert not componenttools.is_well_formed_component(t)
