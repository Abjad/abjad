# -*- coding: utf-8 -*-
import abjad


def test_instrumenttools_InstrumentList_name_to_instrument_01():

    instruments = abjad.instrumenttools.InstrumentList()
    name = 'Clarinet in B-flat'
    instrument = instruments._name_to_instrument(name)
    assert instrument == abjad.instrumenttools.ClarinetInBFlat()


def test_instrumenttools_InstrumentList_name_to_instrument_02():

    instruments = abjad.instrumenttools.InstrumentList()
    name = 'Clarinet in E-flat'
    instrument = instruments._name_to_instrument(name)
    assert instrument == abjad.instrumenttools.ClarinetInEFlat()
