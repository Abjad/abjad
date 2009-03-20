from abjad import *
import py.test


py.test.skip('Spanner changes.')

def test_spanner_component_to_left_of_index_01( ):

   t = Voice(scale(4))
   p = Beam(t[:])

   assert p._componentToLeftOfIndex(0) is None
   assert p._componentToLeftOfIndex(1) is p[0]
   assert p._componentToLeftOfIndex(2) is p[1]
   assert p._componentToLeftOfIndex(3) is p[2]
   assert p._componentToLeftOfIndex(4) is p[3]
   assert p._componentToLeftOfIndex(99) is p[3]


def test_spanner_component_to_left_of_index_02( ):

   p = Beam([ ])

   assert p._componentToLeftOfIndex(0) is None
   assert p._componentToLeftOfIndex(1) is None
   assert p._componentToLeftOfIndex(99) is None
