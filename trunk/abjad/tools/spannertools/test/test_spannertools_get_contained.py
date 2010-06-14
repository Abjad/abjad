from abjad import *
import py.test


def test_spannertools_get_contained_01( ):
   '''Return unordered set of spanners contained
      within any of the list of thread-contiguous components.'''

   t = Voice(Container(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)
   beam = Beam(t[0][:])
   slur = Slur(t[1][:])
   trill = Trill(t.leaves)

   r'''
   \new Voice {
           {
                   c'8 [ \startTrillSpan
                   d'8 ]
           }
           {
                   e'8 (
                   f'8 ) \stopTrillSpan
           }
   }
   '''

   spanners = spannertools.get_contained([t])
   assert len(spanners) == 3
   assert beam in spanners
   assert slur in spanners
   assert trill in spanners

   spanners = spannertools.get_contained(t.leaves)
   assert len(spanners) == 3
   assert beam in spanners
   assert slur in spanners
   assert trill in spanners

   spanners = spannertools.get_contained(t[0:1])
   assert len(spanners) == 2
   assert beam in spanners
   assert trill in spanners

   spanners = spannertools.get_contained(t.leaves[0:1])
   assert len(spanners) == 2
   assert beam in spanners
   assert trill in spanners
