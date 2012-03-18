from abc import ABCMeta
from abc import abstractmethod
from abjad.tools.pitchtools._Harmonic import _Harmonic
from abjad.tools.pitchtools._Interval import _Interval


class _HarmonicInterval(_Interval, _Harmonic):
    '''..versionadded:: 2.0

    Harmonic interval base class.
    '''
    __metaclass__ = ABCMeta
