from abjad.tools.instrumenttools._Instrument import _Instrument


class _BrassInstrument(_Instrument):
    '''.. versionadded:: 2.0

    Abjad model of brass instruments.
    '''

    def __init__(self, **kwargs):
        _Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'brass instrument'
        self._default_performer_names.append('brass player')
