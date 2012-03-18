from abjad import *


def test_instrumenttools_Flute_instrument_name_markup_01():

    flute = instrumenttools.Flute()
    assert flute.instrument_name_markup == markuptools.Markup('Flute')

    flute = instrumenttools.Flute(instrument_name='foo')
    assert flute.instrument_name_markup == markuptools.Markup('Foo')
    
    flute = instrumenttools.Flute(instrument_name_markup=markuptools.Markup('foo'))
    assert flute.instrument_name_markup == markuptools.Markup('foo')
