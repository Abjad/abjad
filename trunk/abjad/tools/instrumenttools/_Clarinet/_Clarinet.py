from abjad.tools.instrumenttools._SingleReedInstrument import _SingleReedInstrument


class _Clarinet(_SingleReedInstrument):
    r'''.. versionadded:: 2.6

    Abjad model of the family of clarinets.
    '''

    def __init__(self, **kwargs):
        _SingleReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'clarinet'
        self._default_performer_names.extend(['clarinettist', 'clarinetist'])
        self._default_short_instrument_name = 'cl.'
