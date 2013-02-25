import abc
from abjad.tools.instrumenttools.BrassInstrument import BrassInstrument


class Trombone(BrassInstrument):
    r'''.. versionadded:: 2.0

    Abjad model of the family of trombones.
    '''

    @abc.abstractmethod
    def __init__(self, **kwargs):
        BrassInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'trombone'
        self._default_performer_names.append('trombonist')
        self._default_short_instrument_name = 'trb.'
