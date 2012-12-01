from experimental import helpertools
from experimental import segmenttools
from experimental.selectortools.TimeRelationTimespanSelector import TimeRelationTimespanSelector
from experimental.selectortools.SliceTimespanSelector import SliceTimespanSelector


class ScoreTimespanSelector(SliceTimespanSelector, TimeRelationTimespanSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select score::

        >>> selectortools.ScoreTimespanSelector()
        ScoreTimespanSelector()
    
    All score selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, time_relation=None, voice_name=None):
        from experimental import specificationtools
        SliceTimespanSelector.__init__(self, voice_name=voice_name)
        TimeRelationTimespanSelector.__init__(self, time_relation=time_relation)
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
