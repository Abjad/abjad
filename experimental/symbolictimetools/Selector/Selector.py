import abc
from experimental.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class Selector(SymbolicTimespan):
    r'''.. versionadded:: 1.0

    Abstract base class from which concrete selectors inherit.
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
