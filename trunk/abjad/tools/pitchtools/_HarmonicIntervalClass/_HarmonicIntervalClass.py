from abc import ABCMeta
from abjad.tools.pitchtools._Harmonic import _Harmonic
from abjad.tools.pitchtools.IntervalObjectClass import IntervalObjectClass


class _HarmonicIntervalClass(IntervalObjectClass, _Harmonic):
    '''.. versionadded:: 2.0

    Harmonic interval-class base class.
    '''
    __metaclass__ = ABCMeta

    pass
