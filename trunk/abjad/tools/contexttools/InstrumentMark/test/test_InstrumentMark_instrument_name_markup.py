from abjad import *


def test_InstrumentMark_instrument_name_markup_01():
    '''Instrument name is read / write.
    '''

    instrument = contexttools.InstrumentMark('Flute', 'Fl.')
    assert instrument.instrument_name_markup == markuptools.Markup('Flute')

    instrument.instrument_name_markup = 'Alto Flute'
    assert instrument.instrument_name_markup == markuptools.Markup('Alto Flute')
