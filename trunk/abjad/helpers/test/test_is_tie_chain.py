from abjad.helpers.is_tie_chain import _is_tie_chain
from abjad import *


def test_is_tie_chain_01( ):
   assert _is_tie_chain(( ))


def test_is_tie_chain_02( ):
   t = Note(0, (1, 4))
   assert _is_tie_chain(t.tie.chain)


def test_is_tie_chain_03( ):
   t = Staff(run(4))
   Tie(t[:2])
   assert _is_tie_chain(t[0].tie.chain)
   assert _is_tie_chain(t[1].tie.chain)
   assert _is_tie_chain(t[2].tie.chain)
   assert _is_tie_chain(t[3].tie.chain)


def test_is_tie_chain_04( ):
   t = Staff(run(4))
   Tie(t[:])
   assert _is_tie_chain(t[0].tie.chain)
   assert _is_tie_chain(t[1].tie.chain)
   assert _is_tie_chain(t[2].tie.chain)
   assert _is_tie_chain(t[3].tie.chain)
