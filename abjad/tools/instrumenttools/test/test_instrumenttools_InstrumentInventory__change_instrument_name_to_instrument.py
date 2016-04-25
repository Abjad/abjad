# -*- coding: utf-8 -*-
from abjad import *


def test_instrumenttools_InstrumentInventory__change_instrument_name_to_instrument_01():

    inventory = instrumenttools.InstrumentInventory()
    name = 'Clarinet in B-flat'
    instrument = inventory._change_instrument_name_to_instrument(name)
    assert instrument == instrumenttools.ClarinetInBFlat()


def test_instrumenttools_InstrumentInventory__change_instrument_name_to_instrument_02():

    inventory = instrumenttools.InstrumentInventory()
    name = 'Clarinet in E-flat'
    instrument = inventory._change_instrument_name_to_instrument(name)
    assert instrument == instrumenttools.ClarinetInEFlat()
