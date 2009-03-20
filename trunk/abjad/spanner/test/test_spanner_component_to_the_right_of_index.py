from abjad import *
import py.test


py.test.skip('Spanner changes.')

def test_spanner_component_to_right_of_index_01( ):

   t = Voice(scale(4))
   p = Beam(t[:])

   assert p._componentToRightOfIndex(0) is p[0]
   assert p._componentToRightOfIndex(1) is p[1]
   assert p._componentToRightOfIndex(2) is p[2]
   assert p._componentToRightOfIndex(3) is p[3]
   assert p._componentToRightOfIndex(4) is None
   assert p._componentToRightOfIndex(99) is None


def test_spanner_component_to_right_of_index_02( ):

   p = Beam([ ])

   assert p._componentToRightOfIndex(0) is None
   assert p._componentToRightOfIndex(1) is None
   assert p._componentToRightOfIndex(99) is None
