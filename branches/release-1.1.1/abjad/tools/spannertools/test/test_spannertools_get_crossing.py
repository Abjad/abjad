from abjad import *
import py.test


def test_spannertools_get_crossing_01( ):
   '''Return unordered set of spanners crossing
      over the begin- or end-bounds of thread-contiguous components.'''

   t = Voice(Container(construct.run(2)) * 2)
   pitchtools.diatonicize(t)
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

   spanners = spannertools.get_crossing([t])
   assert spanners == set([ ])

   spanners = spannertools.get_crossing(t.leaves)
   assert spanners == set([ ])

   spanners = spannertools.get_crossing(t[0:1])
   assert len(spanners) == 1
   assert trill in spanners

   spanners = spannertools.get_crossing(t.leaves[0:1])
   assert len(spanners) == 2
   assert beam in spanners
   assert trill in spanners


def test_spannertools_get_crossing_02( ):
   '''Trying to get crossing spanners across 
      non-thread-contiguous components raises ContiguityError.'''

   t = Container(Voice(construct.run(2)) * 2)
   pitchtools.diatonicize(t)
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
   
   assert py.test.raises(ContiguityError, 'spannertools.get_crossing(t.leaves)')


def test_spannertools_get_crossing_03( ):
   '''Helper gets spanners that cross in from above.'''

   t = Voice(RigidMeasure((2, 8), construct.run(2)) * 3)
   pitchtools.diatonicize(t)
   beam = Beam(t[1:2] + t[2][0:1])

   r'''\new Voice {
         \time 2/8
         c'8
         d'8
         \time 2/8
         e'8 [
         f'8
         \time 2/8
         g'8 ]
         a'8
   }'''

   spanners = spannertools.get_crossing(t.leaves)

   assert len(spanners) == 1
   assert beam in spanners
