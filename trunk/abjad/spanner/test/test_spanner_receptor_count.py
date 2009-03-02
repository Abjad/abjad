from abjad import *


def test_spanner_receptor_count_01( ):
   '''Return 0 when no spanners attach.'''
   
   t = Staff(scale(4))
   assert t[0].beam.count == 0
   assert t[0].dynamics.count == 0
   assert t[0].glissando.count == 0
   assert t[0].tie.count == 0


def test_spanner_receptor_count_02( ):
   '''Return 1 when one spanner attaches.'''
   
   t = Staff(scale(4))
   Crescendo(t[:])
   assert t[0].beam.count == 0
   assert t[0].dynamics.count == 1
   assert t[0].glissando.count == 0
   assert t[0].tie.count == 0
