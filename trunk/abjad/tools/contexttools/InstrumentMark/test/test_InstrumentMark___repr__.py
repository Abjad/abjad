from abjad import *
from abjad.tools.contexttools import InstrumentMark


def test_InstrumentMark___repr___01( ):
   '''Instrument mark repr is evaluable.
   '''

   instrument_mark_1 = contexttools.InstrumentMark('Flute', 'Fl.')
   instrument_mark_2 = eval(repr(instrument_mark_1))

   assert isinstance(instrument_mark_1, contexttools.InstrumentMark)
   assert isinstance(instrument_mark_2, contexttools.InstrumentMark)
