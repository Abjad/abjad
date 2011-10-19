from abjad import *


def test_instrumenttools_list_instrument_names_01():

    instrument_names = instrumenttools.list_instrument_names()

    assert all([isinstance(x, str) for x in instrument_names])
