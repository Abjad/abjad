from abjad import *


def test_instrumenttools_UntunedPercussion___repr___01():
    '''Without instrument name.
    '''

    instrument = instrumenttools.UntunedPercussion()

    assert repr(instrument) == 'UntunedPercussion()'
    assert instrument._storage_format == 'instrumenttools.UntunedPercussion()'

    
def test_instrumenttools_UntunedPercussion___repr___02():
    '''With instrument name and short instrument name.
    '''

    instrument = instrumenttools.UntunedPercussion()
    instrument.instrument_name = 'rattle'
    instrument.short_instrument_name = 'rt.'

    assert repr(instrument) == "UntunedPercussion(instrument_name='rattle', short_instrument_name='rt.')"
    assert instrument._storage_format == "instrumenttools.UntunedPercussion(\n\tinstrument_name='rattle',\n\tshort_instrument_name='rt.'\n\t)"
