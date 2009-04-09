from abjad import *
from abjad.tools import construct


def test_tietools_duration_change_01( ):
   '''Change length-1 tie chain to length-2 tie chain.'''

   t = Staff(run(1))
   Beam(t[:])
   tietools.duration_change(t[0].tie.chain, Rational(5, 32))

   r'''\new Staff {
      c'8 [ ~
      c'32 ]
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ~\n\tc'32 ]\n}"


def test_tietools_duration_chnage_02( ):
   '''Change length-2 tie chain to length-1 tie chain.'''

   t = Staff(construct.notes(0, [(5, 32)]))
   Beam(t[:])
   tietools.duration_change(t[0].tie.chain, Rational(4, 32))

   r'''\new Staff {
      c'8 [ ]
   }'''

   assert check(t)
   assert t.format == "\\new Staff {\n\tc'8 [ ]\n}"
