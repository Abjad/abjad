# -*- coding: utf-8 -*-
from abjad import *


def test_instrumenttools_Instrument__default_instrument_name_to_instrument_class_01():

    instrument_class = \
        instrumenttools.Instrument._default_instrument_name_to_instrument_class(
            'clarinet in E-flat')
    assert instrument_class == instrumenttools.ClarinetInEFlat


def test_instrumenttools_Instrument__default_instrument_name_to_instrument_class_02():

    assert instrumenttools.Instrument._default_instrument_name_to_instrument_class(
        'foo') is None
