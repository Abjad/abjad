import abc
import numbers
from abjad.tools.abctools.AbjadObject import AbjadObject


class SymbolicTimespan(AbjadObject):
    r'''.. versionadded:: 1.0

    Abstract base class from which conrete symbolic timespans inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

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

    ### PUBLIC METHODS ###

    def adjust_offsets(self, start=None, stop=None):
        '''Set offsets on self.
        '''
        from experimental import symbolictimetools
        assert isinstance(start, (numbers.Number, tuple, type(None))), repr(start)
        assert isinstance(stop, (numbers.Number, tuple, type(None))), repr(stop)
        return symbolictimetools.OffsetOperator(self, start_offset=start, stop_offset=stop)

    def divide_by_ratio(self, ratio):
        ''''Divide self by `ratio`.

        Method is mirrors ``mathtools.divide_number_by_ratio()``.

        Return tuple of timespans.
        '''
        from experimental import symbolictimetools
        result = []
        for part in range(len(ratio)):
            # TODO: eventually create custom class different from TimeRatioOperator
            result.append(symbolictimetools.TimeRatioOperator(self, ratio, part))
        return tuple(result)

    def get_duration(self, score_specification, context_name):
        '''Evaluate duration of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return duration.
        '''
        start_offset, stop_offset = self.get_offsets(score_specification, context_name)
        return stop_offset - start_offset

    @abc.abstractmethod
    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        '''Get start offset and stop offset of symbolic timespan
        when applied to `context_name` in `score_specification`.

        Return pair.
        '''
        pass

#    @abc.abstractmethod
#    def set_segment_identifier(self, segment_identifier):
#        '''Delegate to ``self.selector.set_segment_identifier()``.
#        '''
#        pass
