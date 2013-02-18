import abc
from abjad.tools.instrumenttools.ReedInstrument import ReedInstrument


class DoubleReedInstrument(ReedInstrument):
    '''.. versionadded:: 2.0

    Abjad model of double-reed instruments.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, **kwargs):
        ReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'double reed instrument'
        self._default_performer_names.append('double reed player')
