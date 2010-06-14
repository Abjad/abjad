from abjad import *


def test_clef_interface__parentCanContribute_01( ):
   '''Leaf two starts *after* parent staff starts.
   Both forced clefs should be obeyed.
   '''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t.clef.forced = Clef('bass')
   t[2].clef.forced = Clef('treble')

   assert t[2].clef._selfCanContribute
   assert not t[2].clef._parentCanContribute
   assert t[2].clef._selfShouldContribute


def test_clef_interface__parentCanContribute_02( ):
   '''Leaf zero starts *at the same time as* parent staff starts.
   Only parent clef should be obeyed.
   '''

   t = Staff(leaftools.make_first_n_notes_in_ascending_diatonic_scale(4))
   t.clef.forced = Clef('bass')
   t[0].clef.forced = Clef('treble')

   assert t[0].clef._selfCanContribute
   assert t[0].clef._parentCanContribute
   assert not t[0].clef._selfShouldContribute
