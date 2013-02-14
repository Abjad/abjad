import abc
from abjad.tools import durationtools
from experimental.tools.handlertools.Handler import Handler


class DynamicHandler(Handler):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, minimum_duration=None):
        self.minimum_duration = minimum_duration

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _tools_package_name(self):
        return 'handlertools.dynamics'

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def minimum_duration():
        def fget(self):
            return self._minimum_duration
        def fset(self, minimum_duration):
            if minimum_duration is None:
                self._minimum_duration = minimum_duration
            else:
                duration = durationtools.duration_token_to_duration_pair(minimum_duration)
                #self._minimum_duration = durationtools.Duration(*duration)
                self._minimum_duration = durationtools.Duration(duration)
