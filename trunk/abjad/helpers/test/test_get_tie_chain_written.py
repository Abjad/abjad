from abjad.helpers.get_tie_chain_written import _get_tie_chain_written
from abjad.tools import construct
from abjad import *


def test_get_tie_chain_written_01( ):
   '''Commonplace tie chain.'''
   t = construct.notes(0, [(5, 16)])
   assert _get_tie_chain_written(t[0].tie.chain) == Rational(5, 16)


def test_get_tie_chain_written_02( ):
   '''Empty tie chain returns 0.'''
   assert _get_tie_chain_written(( )) == 0


def test_get_tie_chain_written_03( ):
   '''Trivial tie chain.'''
   t = Note(0, (1, 4))
   assert _get_tie_chain_written(t.tie.chain) == Rational(1, 4)
