import abc
from abjad.tools.instrumenttools.ReedInstrument import ReedInstrument


class SingleReedInstrument(ReedInstrument):
    '''.. versionadded:: 2.0

    Abjad model of single-reed instruments.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, **kwargs):
        ReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'single reed instrument'
        self._default_performer_names.append('single reed player')
