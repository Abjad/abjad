# -*- encoding: utf-8 -*-
from abjad import *
from abjad.tools.instrumenttools.Instrument import Instrument


def test_instrumenttools_Instrument_list_instruments_01():

    instruments = instrumenttools.Instrument._list_instruments()

    assert all(issubclass(x, Instrument) for x in instruments)
