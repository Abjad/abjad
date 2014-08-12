# -*- encoding: utf-8 -*-
import abc
from abjad.tools import durationtools
from abjad.tools.handlertools.Handler import Handler


class DynamicHandler(Handler):
    r'''Dynamic handler.
    '''

    ### CLASS VARIABLES ###

    __metaclass__ = abc.ABCMeta

    __slots__ = (
        '_minimum_duration',
        )

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, minimum_duration=None):
        Handler.__init__(self)
        if minimum_duration is not None:
            minimum_duration = durationtools.Duration(minimum_duration)
        self._minimum_duration = minimum_duration

    ### PUBLIC PROPERTIES ###

    @property
    def minimum_duration(self):
        r'''Gets minimum duration of duration handler.

        Returns duration or none.
        '''
        return self._minimum_duration