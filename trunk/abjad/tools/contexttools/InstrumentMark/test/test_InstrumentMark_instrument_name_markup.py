from abjad import *


def test_InstrumentMark_instrument_name_markup_01():
    '''Instrument name is read / write.
    '''

    instrument = contexttools.InstrumentMark('flute', 'fl.')
    assert instrument.instrument_name_markup == markuptools.Markup('flute')

    instrument.instrument_name_markup = 'alto flute'
    assert instrument.instrument_name_markup == markuptools.Markup('alto flute')

    instrument.instrument_name_markup = markuptools.Markup('foo')
    assert instrument.instrument_name_markup == markuptools.Markup('foo')
