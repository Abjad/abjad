from abjad import *


def test_spannertools_get_attached_01( ):
   '''Get all spanners attaching directly to any component in list.'''

   t = Staff(scale(4))
   b1 = Beam(t[:2])
   b2 = Beam(t[2:])
   crescendo = Crescendo(t)

   r'''
   \new Staff {
      c'8 [ \<
      d'8 ]
      e'8 [
      f'8 ] \!
   }
   '''

   spanners = spannertools.get_attached(t[:])

   assert b1 in spanners
   assert b2 in spanners
   assert crescendo not in spanners

   
def test_spannertools_get_attached_02( ):
   '''Accept empty component list.'''

   spanners = spannertools.get_attached([ ])
   
   assert spanners == set([ ])


def test_spannertools_get_attached_03( ):
   '''Return empty set when no spanners.'''

   t = Staff(scale(4))
   spanners = spannertools.get_attached(t[:])

   assert spanners == set([ ])
