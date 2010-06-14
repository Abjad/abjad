from abjad import *


def test_tempo_spanner_overlap_01( ):
   '''Overlapping tempo spanners are not well formed.'''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   TempoSpanner(t[:])
   TempoSpanner(t[:])

   assert not check.wf(t)
