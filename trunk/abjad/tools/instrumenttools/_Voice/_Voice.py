import abc
from abjad.tools.instrumenttools._Instrument import _Instrument


class _Voice(_Instrument):
    r'''.. versionadded:: 2.8

    Abjad model of the human voice.
    '''

    __metaclass__ = abc.ABCMeta

    def __init__(self, **kwargs):
        _Instrument.__init__(self, **kwargs)
        self._default_instrument_name = 'voice'
        self._default_performer_names.append('vocalist')
