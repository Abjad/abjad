import abc
from abjad.tools.instrumenttools.Instrument import Instrument


class Voice(Instrument):
    r'''.. versionadded:: 2.8

    Abjad model of the human voice.
    '''

    @abc.abstractmethod
    def __init__(self, **kwargs):
        Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'voice'
        self._default_performer_names.append('vocalist')
