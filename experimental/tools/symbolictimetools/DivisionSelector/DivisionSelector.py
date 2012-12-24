from abjad.tools import durationtools
from abjad.tools import selectiontools
from abjad.tools import timerelationtools
from abjad.tools import timespantools
from experimental.tools import divisiontools
from experimental.tools.symbolictimetools.VoiceSelector import VoiceSelector


class DivisionSelector(VoiceSelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental.tools import *

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
    
    ### PRIVATE METHODS ###

    def _get_offsets(self, score_specification, voice_name):
        '''Evaluate start and stop offsets of selector when applied
        to `voice_name` in `score_specification`.

        Return offset pair.
        '''
        voice_division_list = score_specification.contexts[voice_name]['voice_division_list']
        divisions = []
        segment_specification = score_specification.get_start_segment_specification(self.anchor)
        start_offset, stop_offset = score_specification.segment_identifier_expression_to_offsets(
            segment_specification.specification_name)
        timespan_1 = timespantools.Timespan(start_offset, stop_offset)
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
        divisions, start_offset = self._apply_modifications(divisions, start_offset)
        start_offset = divisions[0].start_offset
        stop_offset = divisions[-1].stop_offset
        start_offset, stop_offset = self._apply_timespan_modifications(start_offset, stop_offset)
        return start_offset, stop_offset
