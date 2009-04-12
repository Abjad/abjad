from abjad import *


def test_spannertools_withdraw_from_covered_01( ):
   '''Withdraw from all spanners covered by components.'''

   t = Voice(scale(4))
   Beam(t[:2])
   Slur(t[:])

   r'''\new Voice {
           c'8 [ (
           d'8 ]
           e'8
           f'8 )
   }'''

   spannertools.withdraw_from_covered(t[:2])

   r'''\new Voice {
           c'8 (
           d'8
           e'8
           f'8 )
   }'''

   assert check.wf(t)
   assert t.format == "\\new Voice {\n\tc'8 (\n\td'8\n\te'8\n\tf'8 )\n}"
