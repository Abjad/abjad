import abc
from abjad.tools.instrumenttools.SingleReedInstrument import SingleReedInstrument


class Saxophone(SingleReedInstrument):
    r'''.. versionadded:: 2.6

    Abjad model of the family of saxophones.
    '''

    @abc.abstractmethod
    def __init__(self, **kwargs):
        SingleReedInstrument.__init__(self, **kwargs)
        self._default_instrument_name = 'saxophone'
        self._default_performer_names.extend(['saxophonist'])
        self._default_short_instrument_name = 'sax.'
