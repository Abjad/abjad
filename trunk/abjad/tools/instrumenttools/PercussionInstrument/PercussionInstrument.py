import abc
from abjad.tools.instrumenttools.Instrument import Instrument


class PercussionInstrument(Instrument):
    '''.. versionadded:: 2.0

    Abjad model of percussion instruments.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'percussion instrument'
        self._default_performer_names.append('percussionist')
