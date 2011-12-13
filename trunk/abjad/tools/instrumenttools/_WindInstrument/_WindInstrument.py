from abjad.tools.instrumenttools._Instrument import _Instrument


class _WindInstrument(_Instrument):
    '''.. versionadded:: 2.0

    Abjad model of the wind instrument.
    '''

    def __init__(self, **kwargs):
        _Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'wind instrument'
        self._default_performer_names.append('wind player')
