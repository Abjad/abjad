from abjad.tools.instrumenttools._Instrument import _Instrument


class _StringInstrument(_Instrument):
    '''.. versionadded:: 2.0

    Abjad model of string instruments.
    '''

    def __init__(self, **kwargs):
        _Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'string instrument'
        self._default_performer_names.append('string player')
