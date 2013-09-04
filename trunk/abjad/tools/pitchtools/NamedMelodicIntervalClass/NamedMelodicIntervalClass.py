# -*- encoding: utf-8 -*-
from abjad.tools.pitchtools.NamedIntervalClass import NamedIntervalClass


class NamedMelodicIntervalClass(NamedIntervalClass):
    '''Abjad model of named melodic interval-class:

    ::

        >>> pitchtools.NamedMelodicIntervalClass('-M9')
        NamedMelodicIntervalClass('-M2')

    Return named melodic interval-class.
    '''

