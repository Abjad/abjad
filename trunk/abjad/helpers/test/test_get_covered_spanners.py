from abjad import *
import py.test


def test_get_covered_spanners_01( ):
   '''Return unordered set of spanners completely covered
      by the time bounds of thread-contiguous components.'''

   t = Voice(Sequential(run(2)) * 2)
   diatonicize(t)
   beam = Beam(t[0][:])
   slur = Slur(t[1][:])
   trill = Trill(t.leaves)

   r'''\new Voice {
           {
                   c'8 [ \startTrillSpan
                   d'8 ]
           }
           {
                   e'8 (
                   f'8 ) \stopTrillSpan
           }
   }'''

   spanners = get_covered_spanners([t])
   assert len(spanners) == 3
   assert beam in spanners
   assert slur in spanners
   assert trill in spanners

   spanners = get_covered_spanners(t.leaves)
   assert len(spanners) == 3
   assert beam in spanners
   assert slur in spanners
   assert trill in spanners

   spanners = get_covered_spanners(t[0:1])
   assert len(spanners) == 1
   assert beam in spanners

   spanners = get_covered_spanners(t.leaves[0:1])
   assert spanners == set([ ])


def test_get_covered_spanners_02( ):
   '''Trying to get covered spanners across 
      non-thread-contiguous components raises ContiguityError.'''

   t = Sequential(Voice(run(2)) * 2)
   diatonicize(t)
   Beam(t.leaves[:2])
   Slur(t.leaves[2:])
   
   r'''{
           \new Voice {
                   c'8 [
                   d'8 ]
           }
           \new Voice {
                   e'8 (
                   f'8 )
           }
   }'''
   
   assert py.test.raises(ContiguityError, 'get_covered_spanners(t.leaves)')
