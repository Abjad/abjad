import abc
from abjad.tools import durationtools
from experimental.handlertools.Handler import Handler


class DynamicHandler(Handler):

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, minimum_prolated_duration=None):
        self.minimum_prolated_duration = minimum_prolated_duration

    ### PRIVATE READ-ONLY PROPERTIES ###

    @property
    def _tools_package_name(self):
        return 'handlertools.dynamics'

    ### READ / WRITE PUBLIC PROPERTIES ###

    @apply
    def minimum_prolated_duration():
        def fget(self):
            return self._minimum_prolated_duration
        def fset(self, minimum_prolated_duration):
            if minimum_prolated_duration is None:
                self._minimum_prolated_duration = minimum_prolated_duration
            else:
                duration = durationtools.duration_token_to_duration_pair(minimum_prolated_duration)
                #self._minimum_prolated_duration = durationtools.Duration(*duration)
                self._minimum_prolated_duration = durationtools.Duration(duration)
