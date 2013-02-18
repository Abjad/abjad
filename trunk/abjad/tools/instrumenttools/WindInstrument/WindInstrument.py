import abc
from abjad.tools.instrumenttools.Instrument import Instrument


class WindInstrument(Instrument):
    '''.. versionadded:: 2.0

    Abjad model of the wind instrument.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'wind instrument'
        self._default_performer_names.append('wind player')
