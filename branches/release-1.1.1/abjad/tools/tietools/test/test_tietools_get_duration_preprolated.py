from abjad import *
from abjad.tools import construct


def test_tietools_get_duration_preprolated_01( ):
   '''Return sum of preprolated durations of leaves in tie chain.'''

   notes = construct.notes(0, [(5, 16)])
   assert tietools.get_duration_preprolated(notes[0].tie.chain) == \
      Rational(5, 16)


def test_tietools_get_duration_preprolated_02( ):
   '''Works on trivial tie chains.'''

   t = Note(0, (1, 4))
   assert tietools.get_duration_preprolated(t.tie.chain) == Rational(1, 4)
