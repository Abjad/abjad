from abjad import *


def testInstrumentMark_instrument_name_markup_01():
    '''Instrument name is read / write.
    '''

    instrument = contexttools.InstrumentMark('flute', 'fl.')
    assert instrument.instrument_name_markup == markuptools.Markup('Flute')

    instrument.instrument_name_markup = 'alto flute'
    assert instrument.instrument_name_markup == markuptools.Markup('alto flute')

    instrument.instrument_name_markup = markuptools.Markup('foo')
    assert instrument.instrument_name_markup == markuptools.Markup('foo')


def testInstrumentMark_instrument_name_markup_02():
    '''Strings are coerced into Markup on instantiation.
    '''
    instrument = contexttools.InstrumentMark('flute', 'fl.', instrument_name_markup='Flute 2')
    assert instrument.instrument_name_markup == markuptools.Markup('Flute 2')
