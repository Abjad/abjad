from abjad import *


def testInstrumentMark_short_instrument_name_markup_01():
    '''Short instrument name is read / write.
    '''

    instrument = contexttools.InstrumentMark('flute', 'fl.')
    assert instrument.short_instrument_name_markup == markuptools.Markup('Fl.')

    instrument.short_instrument_name_markup = 'alto fl.'
    assert instrument.short_instrument_name_markup == markuptools.Markup('alto fl.')

    instrument.short_instrument_name_markup = markuptools.Markup('foo')
    assert instrument.short_instrument_name_markup == markuptools.Markup('foo')


def testInstrumentMark_short_instrument_name_markup_02():
    '''Strings are coerced into Markup on instantiation.
    '''
    instrument = contexttools.InstrumentMark('flute', 'fl.', 
        short_instrument_name_markup='Fl. 2')
    assert instrument.short_instrument_name_markup == markuptools.Markup('Fl. 2')

