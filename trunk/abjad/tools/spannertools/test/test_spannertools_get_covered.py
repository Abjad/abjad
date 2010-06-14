from abjad import *
import py.test


def test_spannertools_get_covered_01( ):
   '''Return unordered set of spanners completely covered
      by the time bounds of thread-contiguous components.'''

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

   spanners = spannertools.get_covered([t])
   assert len(spanners) == 3
   assert beam in spanners
   assert slur in spanners
   assert trill in spanners

   spanners = spannertools.get_covered(t.leaves)
   assert len(spanners) == 3
   assert beam in spanners
   assert slur in spanners
   assert trill in spanners

   spanners = spannertools.get_covered(t[0:1])
   assert len(spanners) == 1
   assert beam in spanners

   spanners = spannertools.get_covered(t.leaves[0:1])
   assert spanners == set([ ])


def test_spannertools_get_covered_02( ):
   '''Trying to get covered spanners across 
      non-thread-contiguous components raises ContiguityError.'''

   t = Container(Voice(leaftools.make_repeated_notes(2)) * 2)
   pitchtools.diatonicize(t)
   Beam(t.leaves[:2])
   Slur(t.leaves[2:])
   
   r'''
   {
           \new Voice {
                   c'8 [
                   d'8 ]
           }
           \new Voice {
                   e'8 (
                   f'8 )
           }
   }
   '''
   
   assert py.test.raises(ContiguityError, 'spannertools.get_covered(t.leaves)')
