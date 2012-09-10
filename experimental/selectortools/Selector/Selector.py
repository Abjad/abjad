import abc
import abc
import abc
from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental import timespantools


class Selector(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which all selectors inherit.
    '''

    ### INITIALIZER ###

    @abc.abstractmethod
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
        '''SingleSourceSymbolicTimespan of selector.

        Return timespan object.
        '''
        return timespantools.SingleSourceSymbolicTimespan(selector=self)

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def get_duration(self, score_specification, context_name):
        r'''Evaluate duration of selector when applied
        to `context_name` in `score_specification`.

        Return duration.
        '''
        raise NotImplementedError

    def get_score_offsets(self, score_specification, context_name):
        r'''Get score start offset and score stop offset of selector when applied
        to `context_name` in `score_specification`.

        Return pair.
        '''
        start_offset = self.get_score_start_offset(score_specification, context_name)
        stop_offset = self.get_score_stop_offset(score_specification, context_name)
        return start_offset, stop_offset

    @abc.abstractmethod
    def get_score_start_offset(self, score_specification, context_name):
        r'''Evaluate score start offset of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        pass

    @abc.abstractmethod
    def get_score_stop_offset(self, score_specification, context_name):
        r'''Evaluate score stop offset of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        pass

    def get_segment_offsets(self, score_specification, context_name):
        r'''Get segment start offset and segment stop offset of selector when applied
        to `context_name` in `score_specification`.

        Return pair.
        '''
        start_offset = self.get_segment_start_offset(score_specification, context_name)
        stop_offset = self.get_segment_stop_offset(score_specification, context_name)
        return start_offset, stop_offset

    @abc.abstractmethod
    def get_segment_start_offset(self, segment_specification, context_name):
        r'''Evaluate segment start offset of selector when applied
        to `context_name` in `segment_specification`.

        Return offset.
        '''
        pass

    @abc.abstractmethod
    def get_segment_stop_offset(self, segment_specification, context_name):
        r'''Evaluate segment stop offset of selector when applied
        to `context_name` in `segment_specification`.

        Return offset.
        '''
        pass
