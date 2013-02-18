import abc
from abjad.tools.instrumenttools.Instrument import Instrument


class ReedInstrument(Instrument):
    '''.. versionadded:: 2.0

    Abjad model of reed instruments.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'reed instrument'
        self._default_performer_names.append('reed player')
