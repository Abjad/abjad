from abjad import *


def test_instrumenttools_list_primary_instruments_01():

    primary_instruments = instrumenttools.list_primary_instruments()

    assert instrumenttools.Piano in primary_instruments
    assert instrumenttools.Guitar in primary_instruments
    assert instrumenttools.Violin in primary_instruments
