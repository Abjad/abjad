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

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        '''True when mandatory and keyword arguments compare equal.
        Otherwise false.

        Return boolean.
        '''
        if not isinstance(expr, type(self)):
            return False
        if not self._mandatory_argument_values == expr._mandatory_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values
        
    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def start_segment_identifier(self):
        '''Selector start segment identifier.

        Raise exception when no start segment identifier can be found.
        '''
        pass

    @abc.abstractproperty
    def stop_segment_identifier(self):
        '''Selector stop segment identifier.

        Raise exception when no start segment identifier can be found.
        '''
        pass

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

    def get_score_start_offset(self, score_specification, context_name):
        r'''Evaluate score start offset of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        segment_start_offset = self.get_segment_start_offset(score_specification, context_name)
        return score_specification.segment_name_and_segment_offset_to_score_offset(
            self.segment_identifier, segment_start_offset)

    def get_score_stop_offset(self, score_specification, context_name):
        r'''Evaluate score stop offset of selector when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        segment_stop_offset = self.get_segment_stop_offset(score_specification, context_name)
        return score_specification.segment_name_and_segment_offset_to_score_offset(
            self.segment_identifier, segment_stop_offset)

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
