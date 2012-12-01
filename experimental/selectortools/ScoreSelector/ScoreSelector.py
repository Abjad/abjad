from experimental import helpertools
from experimental import segmenttools
from experimental.selectortools.TimeRelationSelector import TimeRelationSelector
from experimental.selectortools.SliceSelector import SliceSelector


class ScoreSelector(SliceSelector, TimeRelationSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select score::

        >>> selectortools.ScoreSelector()
        ScoreSelector()
    
    All score selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, time_relation=None, voice_name=None):
        from experimental import specificationtools
        SliceSelector.__init__(self, voice_name=voice_name)
        TimeRelationSelector.__init__(self, time_relation=time_relation)
        self._klass = specificationtools.ScoreSpecification

    ### PUBLIC PROPERTIES ###

    def get_offsets(self, score_specification, context_name):
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
