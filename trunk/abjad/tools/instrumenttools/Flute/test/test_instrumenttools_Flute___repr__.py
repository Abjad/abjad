from abjad import *


def test_instrumenttools_Flute___repr___01():
    '''Unmodified.
    '''

    flute = instrumenttools.Flute()
    assert repr(flute) == 'Flute()'


def test_instrumenttools_Flute___repr___02():
    '''Initializer combinations.
    '''

    flute = instrumenttools.Flute(instrument_name='foo')
    assert repr(flute) == "Flute(instrument_name='foo')"

    flute = instrumenttools.Flute(instrument_name_markup=markuptools.Markup('foo'))
    assert repr(flute) == "Flute(instrument_name_markup=Markup(('foo',)))"
    
    flute = instrumenttools.Flute(short_instrument_name='f.')
    assert repr(flute) == "Flute(short_instrument_name='f.')"

    flute = instrumenttools.Flute(short_instrument_name_markup=markuptools.Markup('f.'))
    assert repr(flute) == "Flute(short_instrument_name_markup=Markup(('f.',)))"


def test_instrumenttools_Flute___repr___03():
    '''Setting combinations.
    '''

    flute = instrumenttools.Flute()
    flute.instrument_name = 'foo'
    assert repr(flute) == "Flute(instrument_name='foo')"

    flute = instrumenttools.Flute()
    flute.instrument_name_markup = markuptools.Markup('foo')
    assert repr(flute) == "Flute(instrument_name_markup=Markup(('foo',)))"
    
    flute = instrumenttools.Flute()
    flute.short_instrument_name = 'f.'
    assert repr(flute) == "Flute(short_instrument_name='f.')"

    flute = instrumenttools.Flute()
    flute.short_instrument_name_markup = markuptools.Markup('f.')
    assert repr(flute) == "Flute(short_instrument_name_markup=Markup(('f.',)))"
