# -*- coding: utf-8 -*-
import abjad


def test_instrumenttools_Instrument__default_instrument_name_to_instrument_class_01():

    instrument_class = \
        abjad.instrumenttools.Instrument._default_instrument_name_to_instrument_class(
            'clarinet in E-flat')
    assert instrument_class == abjad.instrumenttools.ClarinetInEFlat


def test_instrumenttools_Instrument__default_instrument_name_to_instrument_class_02():

    assert abjad.instrumenttools.Instrument._default_instrument_name_to_instrument_class(
        'foo') is None
