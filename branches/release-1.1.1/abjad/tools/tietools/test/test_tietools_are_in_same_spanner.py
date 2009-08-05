from abjad import *


def test_tietools_are_in_same_spanner_01( ):
   '''True if all components in list share same tie spanner.'''

   t = Voice(construct.run(4))
   Tie(t[:2])

   r'''\new Voice {
      c'8 ~
      c'8
      c'8
      c'8
   }'''

   assert tietools.are_in_same_spanner(t[:2])
   assert not tietools.are_in_same_spanner(t[-2:])
   assert tietools.are_in_same_spanner(t[:1])
   assert not tietools.are_in_same_spanner(t[-1:])
   assert not tietools.are_in_same_spanner(t[:])
