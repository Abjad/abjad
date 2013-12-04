# -*- encoding: utf-8 -*-
from abjad import *


def test_instrumenttools_Flute_instrument_name_markup_01():

    flute = instrumenttools.Flute()
    assert flute.instrument_name_markup == markuptools.Markup('Flute')

    flute = instrumenttools.Flute(instrument_name='foo')
    assert flute.instrument_name == 'foo'
    assert flute.instrument_name_markup == markuptools.Markup('Foo')

    foo_markup = markuptools.Markup('foo')

    flute = instrumenttools.Flute(instrument_name_markup=foo_markup)
    assert flute.instrument_name == 'flute'
    assert flute.instrument_name_markup == foo_markup

    flute = instrumenttools.Flute(
        instrument_name='foo',
        instrument_name_markup=foo_markup,
        )
    assert flute.instrument_name == 'foo'
    assert flute.instrument_name_markup == foo_markup
