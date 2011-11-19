from abjad import *


def test_InstrumentMark_short_instrument_name_markup_01():
    '''Short instrument name is read / write.
    '''

    instrument = contexttools.InstrumentMark('Flute', 'Fl.')
    assert instrument.short_instrument_name_markup == markuptools.Markup('Fl.')

    instrument.short_instrument_name_markup = 'Alto Fl.'
    assert instrument.short_instrument_name_markup == markuptools.Markup('Alto Fl.')
