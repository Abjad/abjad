from abjad import *
from abjad.tools import construct


def test_tie_chain_get_leaves_01( ):
   '''Leaves from nontrivial tie chain.'''

   notes = construct.notes(0, [(5, 32)])
   assert tie_chain_get_leaves(notes[0].tie.chain) == notes


def test_tie_chain_get_leaves_02( ):
   '''Leaves from trivial tie chain.'''

   t = Note(0, (1, 4))
   assert tie_chain_get_leaves(t.tie.chain) == [t]
