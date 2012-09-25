import abc
from abjad.tools.abctools.AbjadObject import AbjadObject


class SymbolicTimespan(AbjadObject):
    r'''.. versionadded:: 1.0

    Base symbolic timespan class from which concrete 
    symbolic timespan classes inherit.
    '''

    ### CLASS ATTRIBUTES ###

    __metaclass__ = abc.ABCMeta

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self):
        pass

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification, context_name):
        '''Evaluate duration of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return duration.
        '''
        stop_offset = self.get_score_stop_offset(score_specification, context_name)
        start_offset = self.get_score_start_offset(score_specification, context_name)
        return stop_offset - start_offset

    @abc.abstractmethod
    def get_score_start_offset(self, score_specification, context_name):
        '''Evaluate score start offset of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        pass

    @abc.abstractmethod
    def get_score_stop_offset(self, score_specification, context_name):
        '''Evaluate score stop offset of symbolic timespan when applied
        to `context_name` in `score_specification`.

        Return offset.
        '''
        pass

    @abc.abstractmethod
    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.selector.set_segment_identifier()``.
        '''
        pass
