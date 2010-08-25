from abjad import *
import py.test
py.test.skip('DEPRECATED.')


def test_ClefInterface__parent_can_contribute_01( ):
   '''Leaf two starts *after* parent staff starts.
   Both forced clefs should be obeyed.
   '''

   t = Staff(macros.scale(4))
   t.clef.forced = stafftools.Clef('bass')
   t[2].clef.forced = stafftools.Clef('treble')

   assert t[2].clef._self_can_contribute
   assert not t[2].clef._parent_can_contribute
   assert t[2].clef._self_should_contribute


def test_ClefInterface__parent_can_contribute_02( ):
   '''Leaf zero starts *at the same time as* parent staff starts.
   Only parent clef should be obeyed.
   '''

   t = Staff(macros.scale(4))
   t.clef.forced = stafftools.Clef('bass')
   t[0].clef.forced = stafftools.Clef('treble')

   assert t[0].clef._self_can_contribute
   assert t[0].clef._parent_can_contribute
   assert not t[0].clef._self_should_contribute
