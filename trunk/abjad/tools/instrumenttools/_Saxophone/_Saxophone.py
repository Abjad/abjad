from abjad.tools.instrumenttools._SingleReedInstrument import _SingleReedInstrument


class _Saxophone(_SingleReedInstrument):
    r'''.. versionadded:: 2.6

    Abjad model of the family of saxophones.
    '''

    def __init__(self, **kwargs):
        _SingleReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'sax.'
