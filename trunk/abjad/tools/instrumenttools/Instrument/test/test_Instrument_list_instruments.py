from abjad import *
from abjad.tools import instrumenttools
from abjad.tools.instrumenttools.Instrument import Instrument


def test_Instrument_list_instruments_01():

    instruments = instrumenttools.Instrument.list_instruments()

    assert all(issubclass(x, Instrument) for x in instruments)
