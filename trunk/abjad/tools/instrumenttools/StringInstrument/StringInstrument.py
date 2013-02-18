import abc
from abjad.tools.instrumenttools.Instrument import Instrument


class StringInstrument(Instrument):
    '''.. versionadded:: 2.0

    Abjad model of string instruments.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'string instrument'
        self._default_performer_names.append('string player')
