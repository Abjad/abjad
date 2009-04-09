from abjad import *
from abjad.tools import construct


def test_tiechaintools_duration_written_01( ):
   '''Return sum of written durations of leaves in tie chain.'''

   notes = construct.notes(0, [(5, 16)])
   assert tiechaintools.duration_written(notes[0].tie.chain) == Rational(5, 16)


def test_tiechaintools_duration_written_02( ):
   '''Works on trivial tie chains.'''

   t = Note(0, (1, 4))
   assert tiechaintools.duration_written(t.tie.chain) == Rational(1, 4)
