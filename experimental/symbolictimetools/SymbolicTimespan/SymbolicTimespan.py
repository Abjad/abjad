import abc
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
