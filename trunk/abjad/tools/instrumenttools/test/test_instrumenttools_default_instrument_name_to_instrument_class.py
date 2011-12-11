from abjad import *


def test_instrumenttools_default_instrument_name_to_instrument_class_01():

    instrument_class = instrumenttools.default_instrument_name_to_instrument_class('clarinet in E-flat')
    assert instrument_class == instrumenttools.EFlatClarinet


def test_instrumenttools_default_instrument_name_to_instrument_class_02():

    assert instrumenttools.default_instrument_name_to_instrument_class('foo') is None
