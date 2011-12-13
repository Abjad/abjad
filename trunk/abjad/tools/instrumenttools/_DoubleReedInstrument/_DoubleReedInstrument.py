from abjad.tools.instrumenttools._ReedInstrument import _ReedInstrument


class _DoubleReedInstrument(_ReedInstrument):
    '''.. versionadded:: 2.0

    Abjad model of double-reed instruments.
    '''

    def __init__(self, **kwargs):
        _ReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'double reed instrument'
        self._default_performer_names.append('double reed player')
