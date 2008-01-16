from abjad import *


def test_beam_spanner_fracture_01( ):
   '''This test shows that fracurting beyond the *first* leaf
      effectively does nothing except to replace an existing
      spanner with an identical new spanner.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert len(t.spanners.get( )) == 1
   old = t.spanners.get( )[0]
   assert old.leaves == t[ : 4]
   old.fracture(0, 'left')
   assert len(t.spanners.get( )) == 1
   new = t.spanners.get( )[0]
   assert new.leaves == old.leaves == t[ : 4]
   assert new != old


def test_beam_spanner_fracture_02( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert len(t.spanners.get( )) == 1
   old = t.spanners.get( )[0]
   assert old.leaves == t[ : 4]
   old.fracture(1, 'left')
   assert len(t.spanners.get( )) == 2
   left, right = t.spanners.get( )
   assert left.leaves == t[0 : 1]
   assert right.leaves == t[1 : 4]


def test_beam_spanner_fracture_03( ):
   '''This test shows that fracurting beyond the *last* leaf
      effectively does nothing except to replace an existing
      spanner with an identical new spanner.'''
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert len(t.spanners.get( )) == 1
   old = t.spanners.get( )[0]
   assert old.leaves == t[ : 4]
   old.fracture(-1, 'right')
   assert len(t.spanners.get( )) == 1
   new = t.spanners.get( )[0]
   assert new.leaves == old.leaves == t[ : 4]
   assert new != old


def test_beam_spanner_fracture_04( ):
   t = Staff([Note(n, (1, 8)) for n in range(8)])
   Beam(t[ : 4])
   assert len(t.spanners.get( )) == 1
   old = t.spanners.get( )[0]
   assert old.leaves == t[ : 4]
   old.fracture(1, 'right')
   assert len(t.spanners.get( )) == 2
   left, right = t.spanners.get( )
   assert left.leaves == t[0 : 2]
   assert right.leaves == t[2 : 4]
