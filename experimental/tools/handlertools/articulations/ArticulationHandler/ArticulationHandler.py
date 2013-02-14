import abc
from abjad.tools import durationtools
from abjad.tools import pitchtools
from experimental.tools.handlertools.Handler import Handler


class ArticulationHandler(Handler):

    ### CLASS ATTRIBUTES ##

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, 
        minimum_duration=None, 
        maximum_duration=None,
        minimum_written_pitch=None, 
        maximum_written_pitch=None):
        if minimum_duration is None:
            self.minimum_duration = minimum_duration
        else:
            self.minimum_duration = durationtools.Duration(minimum_duration)
        if maximum_duration is None:
            self.maximum_duration = maximum_duration
        else:
            self.maximum_duration = durationtools.Duration(maximum_duration)
        if minimum_written_pitch is None:
            self.minimum_written_pitch = minimum_written_pitch
        else:
            self.minimum_written_pitch = pitchtools.NamedChromaticPitch(minimum_written_pitch)
        if maximum_written_pitch is None:
            self.maximum_written_pitch = maximum_written_pitch
        else:
            self.maximum_written_pitch = pitchtools.NamedChromaticPitch(maximum_written_pitch)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _tools_package_name(self):
        return 'handlertools.articulations'
