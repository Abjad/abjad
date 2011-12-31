from abjad.tools.instrumenttools._BrassInstrument import _BrassInstrument


class _Trombone(_BrassInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the family of trombones.
    '''

    def __init__(self, **kwargs):
        _BrassInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'trombone'
        self._default_performer_names.append('trombonist')
        self._default_short_instrument_name = 'trb.'
