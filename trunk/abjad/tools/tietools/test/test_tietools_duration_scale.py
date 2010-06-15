from abjad import *


def test_tietools_duration_scale_01( ):
   '''Scale trivial tie chain to nontrivial tie chain.'''

   t = Staff(leaftools.make_repeated_notes(1))
   Beam(t[:])
   tietools.duration_scale(t[0].tie.chain, Rational(5, 4))

   r'''
   \new Staff {
      c'8 [ ~
      c'32 ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ~\n\tc'32 ]\n}"


def test_tietools_duration_scale_02( ):
   '''Scale nontrivial tie chain to trivial tie chain.'''

   t = Staff(leaftools.make_notes(0, [(5, 32)]))
   Beam(t[:])
   tietools.duration_scale(t[0].tie.chain, Rational(4, 5))

   r'''
   \new Staff {
      c'8 [ ]
   }
   '''

   assert componenttools.is_well_formed_component(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n}"
