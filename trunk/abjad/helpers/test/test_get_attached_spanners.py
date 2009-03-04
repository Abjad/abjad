from abjad.helpers.get_attached_spanners import _get_attached_spanners
from abjad import *


def test_get_attached_spanners_01( ):
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

   spanners = _get_attached_spanners(t[:])

   assert b1 in spanners
   assert b2 in spanners
   assert crescendo not in spanners

   
def test_get_attached_spanners_02( ):
   '''Accept empty component list.'''

   spanners = _get_attached_spanners([ ])
   
   assert spanners == set([ ])


def test_get_attached_spanners_03( ):
   '''Return empty set when no spanners.'''

   t = Staff(scale(4))
   spanners = _get_attached_spanners(t[:])

   assert spanners == set([ ])
