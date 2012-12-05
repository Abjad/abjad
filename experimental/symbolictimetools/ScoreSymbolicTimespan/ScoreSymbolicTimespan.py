from experimental import helpertools
from experimental import segmenttools
from experimental.symbolictimetools.TimeRelationSymbolicTimespan import TimeRelationSymbolicTimespan


class ScoreSymbolicTimespan(TimeRelationSymbolicTimespan):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select score::

        >>> symbolictimetools.ScoreSymbolicTimespan()
        ScoreSymbolicTimespan()
    
    All score selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, time_relation=None, voice_name=None):
        from experimental import specificationtools
        TimeRelationSymbolicTimespan.__init__(self, voice_name=voice_name, time_relation=time_relation)
        self._klass = specificationtools.ScoreSpecification

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
