# -*- encoding: utf-8 -*-
import abc
from abjad.tools import durationtools
from abjad.tools import pitchtools
from abjad.tools.handlertools.Handler import Handler


class ArticulationHandler(Handler):
    r'''Articulation handler.
    '''

    ### CLASS VARIABLES ##

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_maximum_duration',
        '_maximum_written_pitch',
        '_minimum_duration',
        '_minimum_written_pitch',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(
        self,
        minimum_duration=None,
        maximum_duration=None,
        minimum_written_pitch=None,
        maximum_written_pitch=None,
        ):
        if minimum_duration is None:
            self._minimum_duration = minimum_duration
        else:
            self._minimum_duration = durationtools.Duration(minimum_duration)
        if maximum_duration is None:
            self._maximum_duration = maximum_duration
        else:
            self._maximum_duration = durationtools.Duration(maximum_duration)
        if minimum_written_pitch is None:
            self._minimum_written_pitch = minimum_written_pitch
        else:
            self._minimum_written_pitch = \
                pitchtools.NamedPitch(minimum_written_pitch)
        if maximum_written_pitch is None:
            self._maximum_written_pitch = maximum_written_pitch
        else:
            self._maximum_written_pitch = \
                pitchtools.NamedPitch(maximum_written_pitch)

    ### PUBLIC PROPERTIES ###

    @property
    def maximum_duration(self):
        r'''Gets maximum duration of handler.

        Returns duration or none.
        '''
        return self._maximum_duration

    @property
    def maximum_written_pitch(self):
        r'''Gets maximum written pitch of handler.

        Returns pitch or none.
        '''
        return self._maximum_written_pitch

    @property
    def minimum_duration(self):
        r'''Gets minimum duration of handler.

        Returns duration or none.
        '''
        return self._minimum_duration

    @property
    def minimum_written_pitch(self):
        r'''Gets minimum written pitch of handler.

        Returns pitch or none.
        '''
        return self._minimum_written_pitch