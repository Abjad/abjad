from abjad import *
from abjad.tools import construct


def test_tiechaintools_duration_scale_01( ):
   '''Scale trivial tie chain to nontrivial tie chain.'''

   t = Staff(run(1))
   Beam(t[:])
   tiechaintools.duration_scale(t[0].tie.chain, Rational(5, 4))

   r'''\new Staff {
      c'8 [ ~
      c'32 ]
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ~\n\tc'32 ]\n}"


def test_tiechaintools_duration_chnage_02( ):
   '''Scale nontrivial tie chain to trivial tie chain.'''

   t = Staff(construct.notes(0, [(5, 32)]))
   Beam(t[:])
   tiechaintools.duration_scale(t[0].tie.chain, Rational(4, 5))

   r'''\new Staff {
      c'8 [ ]
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n}"
