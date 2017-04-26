# -*- coding: utf-8 -*-
from abjad import *


def test_instrumenttools_InstrumentList__change_instrument_name_to_instrument_01():

    instruments = instrumenttools.InstrumentList()
    name = 'Clarinet in B-flat'
    instrument = instruments._change_instrument_name_to_instrument(name)
    assert instrument == instrumenttools.ClarinetInBFlat()


def test_instrumenttools_InstrumentList__change_instrument_name_to_instrument_02():

    instruments = instrumenttools.InstrumentList()
    name = 'Clarinet in E-flat'
    instrument = instruments._change_instrument_name_to_instrument(name)
    assert instrument == instrumenttools.ClarinetInEFlat()
