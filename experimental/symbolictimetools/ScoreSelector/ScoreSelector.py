from experimental import helpertools
from experimental import segmenttools
from experimental.symbolictimetools.Selector import Selector


class ScoreSelector(Selector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Score selector::

        >>> symbolictimetools.ScoreSelector()
        ScoreSelector()
    
    All score selector properties are read-only.
    '''

    ### PUBLIC METHODS ###

    def get_offsets(self, score_specification, context_name):
        '''Return `score_specification` start and stop offsets.
    
        Ignore `context_name` and `start_segment_name`.
        '''
        return score_specification.offsets

    def get_selected_objects(self, score_specification, context_name):
        '''Return `score_specification` unchanged.

        Ignore `context_name`.
        '''
        return selectiontools.Selection([score_specification])
