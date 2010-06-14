from abjad import *


def test_tietools_is_chain_01( ):
   assert tietools.is_chain(( ))


def test_tietools_is_chain_02( ):
   t = Note(0, (1, 4))
   assert tietools.is_chain(t.tie.chain)


def test_tietools_is_chain_03( ):
   t = Staff(leaftools.make_repeated_notes(4))
   Tie(t[:2])
   assert tietools.is_chain(t[0].tie.chain)
   assert tietools.is_chain(t[1].tie.chain)
   assert tietools.is_chain(t[2].tie.chain)
   assert tietools.is_chain(t[3].tie.chain)


def test_tietools_is_chain_04( ):
   t = Staff(leaftools.make_repeated_notes(4))
   Tie(t[:])
   assert tietools.is_chain(t[0].tie.chain)
   assert tietools.is_chain(t[1].tie.chain)
   assert tietools.is_chain(t[2].tie.chain)
   assert tietools.is_chain(t[3].tie.chain)
