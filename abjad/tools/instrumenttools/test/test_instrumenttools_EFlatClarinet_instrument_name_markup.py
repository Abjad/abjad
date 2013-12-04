# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_EFlatClarinet_instrument_name_markup_01():
    r'''By default instrument name markup equals instrument name
    with first character capitalized.
    '''

    clarinet = instrumenttools.EFlatClarinet()
    assert clarinet.instrument_name == 'clarinet in E-flat'

    markup = markuptools.Markup(stringtools.capitalize_string_start(clarinet.instrument_name))
    assert clarinet.instrument_name_markup == markup


def test_instrumenttools_EFlatClarinet_instrument_name_markup_02():
    r'''When user has not set instrument name markup explicitly,
    instrument name changes effect instrument name markup changes
    '''

    clarinet = instrumenttools.EFlatClarinet()
    clarinet.instrument_name == 'foo bar'

    markup = markuptools.Markup(stringtools.capitalize_string_start(clarinet.instrument_name))
    assert clarinet.instrument_name_markup == markup
