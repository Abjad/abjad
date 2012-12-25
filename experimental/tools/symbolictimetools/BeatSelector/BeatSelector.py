from abjad.tools import mathtools
from abjad.tools import sequencetools
from experimental.tools.symbolictimetools.VoiceSelector import VoiceSelector


class BeatSelector(VoiceSelector):
    '''.. versionadded:: 1.0

    Beat selector.

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` beats that start during segment ``'red'``::

        >>> red_segment.select_beats('Voice 1')
        BeatSelector(anchor='red', voice_name='Voice 1')

    Beat selectors are to be treated as immutable.
    '''

    ### PRIVATE METHODS ###

    def _get_offsets(self, score_specification, voice_name):
        '''Evaluate start and stop offsets of selector when applied
        to `voice_name` in `score_specification`.

        Return offset pair.
        '''
        raise NotImplementedError('implement me')
