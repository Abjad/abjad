from abjad import *


def test_InstrumentMark_short_instrument_name_01():
    '''Short instrument name is read / write.
    '''

    instrument = contexttools.InstrumentMark('Flute', 'Fl.')
    assert instrument.short_instrument_name == 'Fl.'

    instrument.short_instrument_name = 'Alto Fl.'
    assert instrument.short_instrument_name == 'Alto Fl.'
