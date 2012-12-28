from abjad.tools import mathtools
from abjad.tools import sequencetools
from experimental.tools.selectortools.Selector import Selector


class BeatSelector(Selector):
    '''

    Beat selector.

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')
    
    Select voice ``1`` beats that start during score::

        >>> selector = score_specification.select_beats('Voice 1')

    ::

        >>> z(selector)
        selectortools.BeatSelector(
            voice_name='Voice 1'
            )

    Select voice ``1`` beats that start during segment ``'red'``::

        >>> selector = red_segment.select_beats('Voice 1')

    ::

        >>> z(selector)
        selectortools.BeatSelector(
            anchor='red',
            voice_name='Voice 1'
            )

    Beat selectors are to be treated as immutable.
    '''

    ### PRIVATE METHODS ###

    def _get_timespan(self, score_specification, voice_name):
        '''Evaluate start and stop offsets of selector when applied
        to `voice_name` in `score_specification`.

        Return offset pair.
        '''
        raise NotImplementedError
