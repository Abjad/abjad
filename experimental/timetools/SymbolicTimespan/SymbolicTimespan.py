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

    # TODO: implement this, make concrete, and remove on child classes
    @abc.abstractmethod
    def get_duration(self, score_specification):
        '''Evaluate duration of symbolic timespan when applied
        to `score_specification`.

        Return duration.
        '''
        pass

    @abc.abstractmethod
    def get_score_start_offset(self, score_specification):
        '''Evaluate score start offset of symbolic timespan when applied
        to `score_specification`.

        Return offset.
        '''
        pass

    @abc.abstractmethod
    def get_score_stop_offset(self, score_specification):
        '''Evaluate score stop offset of symbolic timespan when applied
        to `score_specification`.

        Return offset.
        '''
        pass
