from abjad import *
from abjad.tools import markuptools


def test_instrumenttools_EnglishHorn_instrument_name_01():

    horn = instrumenttools.EnglishHorn()
    assert horn.default_instrument_name == 'English horn'
    assert horn.default_short_instrument_name == 'Eng. hn.'
    assert horn.instrument_name == 'English horn'
    assert horn.short_instrument_name == 'Eng. hn.'
    assert horn.instrument_name_markup == markuptools.Markup('English horn')
    assert horn.short_instrument_name_markup == markuptools.Markup('Eng. hn.')


def test_instrumenttools_EnglishHorn_instrument_name_02():

    horn = instrumenttools.EnglishHorn()
    horn.instrument_name = 'Horn I'
    horn.short_instrument_name = 'Hn. I'

    assert horn.default_instrument_name == 'English horn'
    assert horn.default_short_instrument_name == 'Eng. hn.'
    assert horn.instrument_name == 'Horn I'
    assert horn.short_instrument_name == 'Hn. I'
    assert horn.instrument_name_markup == markuptools.Markup('Horn I')
    assert horn.short_instrument_name_markup == markuptools.Markup('Hn. I')
