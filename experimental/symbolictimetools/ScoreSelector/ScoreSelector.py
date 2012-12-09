from experimental import helpertools
from experimental import segmenttools
from experimental.symbolictimetools.SymbolicTimespan import SymbolicTimespan


class ScoreSelector(SymbolicTimespan):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Score symbolic timespan::

        >>> symbolictimetools.ScoreSelector()
        ScoreSelector()
    
    All score symbolic timespan properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self):
        from experimental import specificationtools
        SymbolicTimespan.__init__(self)
        self._klass = specificationtools.ScoreSpecification

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def anchor(self):
        return

    @property
    def start_segment_identifier(self):
        '''Start segment identifer of none means score-anchoring.
        
        Return none.
        '''
        return

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name, start_segment_name=None):
        '''Evaluate start and stop offsets of selector when applied
        to `score_specification`.
    
        Maybe ignore `context_name`.

        Return offset pair.
        '''
        return score_specification.offsets

    def get_selected_objects(self, score_specification, context_name):
        '''Get segments selected when selector is applied
        to `score_specification`.

        Ignore `context_name`.

        Return list of segments.
        '''
        raise NotImplementedError
