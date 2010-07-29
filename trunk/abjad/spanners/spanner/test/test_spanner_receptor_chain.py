from abjad import *


def test_spanner_receptor_chain_01( ):
   '''Return tuple of all leaves in spanner, if spanned;
      otherwise return 1-tuple of client.'''

   t = Staff(macros.scale(4))
   Beam(t[2:])

   r'''
   \new Staff {
           c'8
           d'8
           e'8 [
           f'8 ]
   } 
   '''

   assert t[0].beam.chain == (t[0], )
   assert t[1].beam.chain == (t[1], )
   assert t[2].beam.chain == (t[2], t[3])
   assert t[3].beam.chain == (t[2], t[3])
