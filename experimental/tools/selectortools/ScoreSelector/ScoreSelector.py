from abjad.tools import timespantools
from experimental.tools import helpertools
from experimental.tools import segmenttools
from experimental.tools.selectortools.Selector import Selector


class ScoreSelector(Selector):
    r'''

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    .. note:: class may be removed.
    
    All score selector properties are read-only.
    '''

    ### PRIVATE METHODS ###

    def _get_timespan(self, score_specification, context_name):
        '''Return `score_specification` start and stop offsets.
    
        Ignore `context_name`.
        '''
        return timespantools.Timespan(*score_specification.offsets)

    def _set_start_segment_identifier(self, segment_identifier):
        raise Exception('{!r} can not be reanchored.'.format(self))
