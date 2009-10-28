from abjad import *


def test_iterate_tie_chains_backward_in_01( ):
   '''Yield successive tie chains.'''

   t = Staff(construct.run(4))
   Tie(t[:2])
   Tie(t[2:])

   r'''
   \new Staff {
           c'8 ~
           c'8
           c'8 ~
           c'8
   }
   '''

   chains = list(iterate.tie_chains_backward_in(t))

   assert chains[0] == (t[2], t[3])
   assert chains[1] == (t[0], t[1])


def test_iterate_tie_chains_backward_in_02( ):
   '''Yield successive tie chains.'''

   t = Staff(construct.run(4))

   r'''
   \new Staff {
           c'8 
           c'8
           c'8 
           c'8
   }
   '''

   chains = list(iterate.tie_chains_backward_in(t))

   assert chains[0] == (t[3], )
   assert chains[1] == (t[2], )
   assert chains[2] == (t[1], )
   assert chains[3] == (t[0], )
