from abjad.tools.instrumenttools._Instrument import _Instrument


class _ReedInstrument(_Instrument):
    '''.. versionadded:: 2.0

    Abjad model of reed instruments.
    '''

    def __init__(self, **kwargs):
        _Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'reed instrument'
        self._default_performer_names.append('reed player')
