# -*- encoding: utf-8 -*-
import abc
from abjad.tools.abctools import AbjadValueObject


class TrackEvent(AbjadValueObject):
    r'''Event in a MIDI track.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_delta_time',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, delta_time=0):
        self._delta_time = delta_time

    ### PUBLIC PROPERTIES ###

    @property
    def delta_time(self):
        r'''Gets track event delta time.
        '''
        return self._delta_time