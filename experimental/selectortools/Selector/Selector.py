from abc import ABCMeta
from abc import abstractmethod
from abc import abstractproperty
from abjad.tools.abctools.AbjadObject import AbjadObject


class Selector(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which all selectors inherit.
    '''

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self):
        pass

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def segment_identifier(self):
        '''Selector segment identifier.

        Raise exception when no segment identifier can be found.
        '''
        raise NotImplementedError("Implement '{}.segment_identifier' soon.".format(self._class_name))

    @property
    def timespan(self):
        '''SingleSourceTimespan of selector.

        Return timespan object.
        '''
        from experimental import timespantools
        return timespantools.SingleSourceTimespan(selector=self)

    ### PUBLIC METHODS ###

    def get_segment_offsets(self, score_specification):
        start_offset = self.get_segment_start_offset(score_specification)
        stop_offset = self.get_segment_stop_offset(score_specification)
        return start_offset, stop_offset
