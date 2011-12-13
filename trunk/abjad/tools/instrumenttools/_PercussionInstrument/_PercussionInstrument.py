from abjad.tools.instrumenttools._Instrument import _Instrument


class _PercussionInstrument(_Instrument):
    '''.. versionadded:: 2.0

    Abjad model of percussion instruments.
    '''

    def __init__(self, **kwargs):
        _Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'percussion instrument'
        self._default_performer_names.append('percussionist')
