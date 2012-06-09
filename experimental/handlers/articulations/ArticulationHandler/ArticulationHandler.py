from abc import ABCMeta
from abc import abstractmethod
from abjad.tools import durationtools
from abjad.tools import pitchtools
from experimental.handlers.Handler import Handler


class ArticulationHandler(Handler):

    ### CLASS ATTRIBUTES ##

    __metaclass__ = ABCMeta

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, 
        minimum_prolated_duration=None, 
        maximum_prolated_duration=None,
        minimum_written_pitch=None, 
        maximum_written_pitch=None):
        if minimum_prolated_duration is None:
            self.minimum_prolated_duration = minimum_prolated_duration
        else:
            self.minimum_prolated_duration = durationtools.Duration(
                *durationtools.duration_token_to_duration_pair(minimum_prolated_duration))
        if maximum_prolated_duration is None:
            self.maximum_prolated_duration = maximum_prolated_duration
        else:
            self.maximum_prolated_duration = durationtools.Duration(
                *durationtools.duration_token_to_duration_pair(maximum_prolated_duration))
        if minimum_written_pitch is None:
            self.minimum_written_pitch = minimum_written_pitch
        else:
            self.minimum_written_pitch = pitchtools.NamedChromaticPitch(minimum_written_pitch)
        if maximum_written_pitch is None:
            self.maximum_written_pitch = maximum_written_pitch
        else:
            self.maximum_written_pitch = pitchtools.NamedChromaticPitch(maximum_written_pitch)

    ### PRIVATE READ-ONLY ATTRIBUTES ###

    @property
    def _tools_package_name(self):
        return 'handlers.articulations'
