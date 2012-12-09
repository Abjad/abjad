import abc
import numbers
#from abjad.tools.abctools.AbjadObject import AbjadObject
from experimental.symbolictimetools.SymbolicTimespan import SymbolicTimespan


#class Selector(AbjadObject):
class Selector(SymbolicTimespan):
    r'''.. versionadded:: 1.0

    Abstract base class from which concrete timespan symbolic timespans inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### READ-ONLY PUBLIC PROPERTIES ###

    @abc.abstractproperty
    def start_segment_identifier(self):
        '''Selector start segment identifier.

        Raise exception when no start segment identifier can be found.
        '''
        pass

    ### PUBLIC METHODS ###

    @abc.abstractmethod
    def get_selected_objects(self, score_specification, context_name):
        '''Get selected objects of symbolic timespan when applied
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
