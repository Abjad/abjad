from abjad import *


def test_instrumenttools_EFlatClarinet_instrument_name_markup_01():
    '''By default instrument name markup equals instrument name
    with first character capitalized.
    '''

    clarinet = instrumenttools.EFlatClarinet()
    assert clarinet.instrument_name == 'clarinet in E-flat'

    markup = markuptools.Markup(iotools.capitalize_string_start(clarinet.instrument_name))
    assert clarinet.instrument_name_markup == markup


def test_instrumenttools_EFlatClarinet_instrument_name_markup_02():
    '''When user has not set instrument name markup explicitly,
    instrument name changes effect instrument name markup changes
    '''

    clarinet = instrumenttools.EFlatClarinet()
    clarinet.instrument_name == 'foo bar'

    markup = markuptools.Markup(iotools.capitalize_string_start(clarinet.instrument_name))
    assert clarinet.instrument_name_markup == markup


def test_instrumenttools_EFlatClarinet_instrument_name_markup_03():
    '''When user has set instrument name markup explicitly,
    instrument name changes do NOT effect instrument name markup.
    '''

    clarinet = instrumenttools.EFlatClarinet()
    clarinet.instrument_name = 'foo bar'
    clarinet.instrument_name_markup = markuptools.Markup('asdf')

    assert clarinet.instrument_name == 'foo bar'
    assert clarinet.instrument_name_markup == markuptools.Markup('asdf')
