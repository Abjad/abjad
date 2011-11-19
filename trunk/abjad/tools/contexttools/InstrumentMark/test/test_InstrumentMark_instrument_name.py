from abjad import *


def test_InstrumentMark_instrument_name_01():
    '''Instrument name is read / write.
    '''

    instrument = contexttools.InstrumentMark('Flute', 'Fl.')
    assert instrument.instrument_name == 'Flute'

    instrument.instrument_name = 'Alto Flute'
    assert instrument.instrument_name == 'Alto Flute'
