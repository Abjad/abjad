from abjad import *
from abjad.tools import markuptools


def test_instrumenttools_FrenchHorn_instrument_name_01():

    horn = instrumenttools.FrenchHorn()
    assert horn.default_instrument_name == 'French horn'
    assert horn.default_short_instrument_name == 'Fr. hn.'
    assert horn.instrument_name == 'French horn'
    assert horn.short_instrument_name == 'Fr. hn.'
    assert horn.instrument_name_markup == markuptools.Markup('French horn')
    assert horn.short_instrument_name_markup == markuptools.Markup('Fr. hn.')


def test_instrumenttools_FrenchHorn_instrument_name_02():

    horn = instrumenttools.FrenchHorn()
    horn.instrument_name = 'horn I'
    horn.short_instrument_name = 'hn. I'

    assert horn.default_instrument_name == 'French horn'
    assert horn.default_short_instrument_name == 'Fr. hn.'
    assert horn.instrument_name == 'horn I'
    assert horn.short_instrument_name == 'hn. I'
    assert horn.instrument_name_markup == markuptools.Markup('Horn I')
    assert horn.short_instrument_name_markup == markuptools.Markup('Hn. I')
