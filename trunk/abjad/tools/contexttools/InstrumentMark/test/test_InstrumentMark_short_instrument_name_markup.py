from abjad import *


def test_InstrumentMark_short_instrument_name_markup_01():
    '''Short instrument name is read / write.
    '''

    instrument = contexttools.InstrumentMark('flute', 'fl.')
    assert instrument.short_instrument_name_markup == markuptools.Markup('fl.')

    instrument.short_instrument_name_markup = 'alto fl.'
    assert instrument.short_instrument_name_markup == markuptools.Markup('alto fl.')

    instrument.short_instrument_name_markup = markuptools.Markup('foo')
    assert instrument.short_instrument_name_markup == markuptools.Markup('foo')
