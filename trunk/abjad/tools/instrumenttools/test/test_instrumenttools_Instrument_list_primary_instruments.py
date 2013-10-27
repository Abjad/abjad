# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Instrument_list_primary_instruments_01():

    primary_instruments = \
        instrumenttools.Instrument._list_primary_instruments()

    assert instrumenttools.Piano in primary_instruments
    assert instrumenttools.Guitar in primary_instruments
    assert instrumenttools.Violin in primary_instruments
