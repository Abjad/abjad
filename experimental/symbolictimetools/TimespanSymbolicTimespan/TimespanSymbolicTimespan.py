import abc
import numbers
from abjad.tools.abctools.AbjadObject import AbjadObject


class TimespanSymbolicTimespan(AbjadObject):
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
        if not self._positional_argument_values == expr._positional_argument_values:
            return False
        return self._keyword_argument_values == expr._keyword_argument_values

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def start_segment_identifier(self):
        '''TimespanSymbolicTimespan start segment identifier.

        Raise exception when no start segment identifier can be found.
        '''
        pass

    @property
    def timespan(self):
        '''SingleSourceSymbolicTimespan of selector.

        Return timespan object.
        '''
        from experimental import symbolictimetools
        return symbolictimetools.SingleSourceSymbolicTimespan(selector=self)

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification, context_name):
        r'''Evaluate duration of selector when applied
        to `context_name` in `score_specification`.

        Return duration.
        '''
        start_offset, stop_offset = self.get_offsets(score_specification, context_name)
        return stop_offset - start_offset

    @abc.abstractmethod
    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        r'''Get start offset and stop offset of selector when applied
        to `context_name` in `score_specification`.

        Return pair.
        '''
        pass
    
    @abc.abstractmethod
    def get_selected_objects(self, score_specification, context_name):
        '''Get selected objects of selector when applied
        to `context_name` in `score_specification`.

        Return object or list of objects.
        '''
        pass        

    ### PUBLIC METHODS ###

    def adjust_offsets(self, start=None, stop=None):
        '''Set offsets on self.
        '''
        from experimental import symbolictimetools
        assert isinstance(start, (numbers.Number, tuple, type(None))), repr(start)
        assert isinstance(stop, (numbers.Number, tuple, type(None))), repr(stop)
        return symbolictimetools.OffsetSymbolicTimespan(self, start_offset=start, stop_offset=stop)

    def divide_by_ratio(self, ratio):
        ''''Divide self by `ratio`.

        Method is mirrors ``mathtools.divide_number_by_ratio()``.

        Return tuple of timespans.
        '''
        from experimental import symbolictimetools
        result = []
        for part in range(len(ratio)):
            # TODO: eventually create custom class different from TimeRatioPartSymbolicTimespan
            result.append(symbolictimetools.TimeRatioPartSymbolicTimespan(self, ratio, part))
        return tuple(result)

    def partition_by_ratio(self, ratio, is_count=True):
        '''Partition self by `ratio`.

        Method mirrors ``sequencetools.partition_sequence_by_ratio_of_lengths()``.
        Method also mirrors ``sequencetools.partition_sequence_by_ratio_of_weights()``.

        Return tuple timespans.
        '''
        from experimental import symbolictimetools
        result = []
        for part in range(len(ratio)):
            if is_count:
                result.append(symbolictimetools.CountRatioPartSymbolicTimespan(self, ratio, part))
            else:
                result.append(symbolictimetools.TimeRatioPartSymbolicTimespan(self, ratio, part))
        return tuple(result)
