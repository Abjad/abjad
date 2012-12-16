from abjad.tools import durationtools
from experimental import divisiontools
from abjad.tools import selectiontools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.symbolictimetools.VoiceSelector import VoiceSelector


class DivisionSelector(VoiceSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all divisions that start during score::

        >>> symbolictimetools.DivisionSelector()
        DivisionSelector()

    Select all divisions that start during segment ``'red'``::

        >>> division_selector = symbolictimetools.DivisionSelector(anchor='red')

    ::

        >>> z(division_selector)
        symbolictimetools.DivisionSelector(
            anchor='red'
            )

    Select the last two divisions that start during segment ``'red'``::

        >>> division_selector = symbolictimetools.DivisionSelector(anchor='red', start_identifier=-2)

    ::

        >>> z(division_selector)
        symbolictimetools.DivisionSelector(
            anchor='red',
            start_identifier=-2
            )

    Division selectors are immutable.
    '''
    
    ### SPECIAL METHODS ###

    # TODO: simplify
    def __deepcopy__(self, memo):
        result = type(self)(
            anchor=self.anchor, 
            start_identifier=self.start_identifier, stop_identifier=self.stop_identifier,
            voice_name=self.voice_name, time_relation=self.time_relation,
            timespan_modifications=self.timespan_modifications,
            selector_modifications=self.selector_modifications)
        result._score_specification = self.score_specification
        return result

    ### PRIVATE METHODS ###

    def _get_offsets(self, score_specification, voice_name):
        '''Evaluate start and stop offsets of selecto when applied
        to `voice_name` in `score_specification`.

        .. note:: add example.

        Return pair.
        '''
        voice_division_list = score_specification.contexts[voice_name]['voice_division_list']
        divisions = []
        segment_specification = score_specification.get_start_segment_specification(self.anchor)
        start_offset, stop_offset = score_specification.segment_identifier_expression_to_offsets(
            segment_specification.specification_name)
        timespan_1 = timespantools.LiteralTimespan(start_offset, stop_offset)
        if self.time_relation is None:
            time_relation = timerelationtools.timespan_2_starts_during_timespan_1(timespan_1=timespan_1)
        else:
            time_relation = self.time_relation
            time_relation._timespan_1 = timespan_1
        for division in voice_division_list:
            if time_relation(timespan_2=division, 
                score_specification=score_specification, 
                context_name=voice_name):
                divisions.append(division)
        divisions = divisions[self.start_identifier:self.stop_identifier]
        start_offset = divisions[0].start_offset
        stop_offset = divisions[-1].stop_offset
        start_offset, stop_offset = self._apply_timespan_modifications(start_offset, stop_offset)
        return start_offset, stop_offset
