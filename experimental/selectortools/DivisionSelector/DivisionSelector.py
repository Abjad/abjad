from abjad.tools import durationtools
from experimental import divisiontools
from abjad.tools import timetools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class DivisionSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import *

    Select all divisions::

        >>> selectortools.DivisionSelector()
        DivisionSelector()

    Select all divisions that start during segment ``'red'``::

        >>> segment = selectortools.SingleSegmentSelector(identifier='red')
        >>> timespan = segment.timespan
        >>> inequality = timetools.timespan_2_starts_during_timespan_1(timespan_1=timespan)

    ::

        >>> division_selector = selectortools.DivisionSelector(inequality=inequality)

    ::

        >>> z(division_selector)
        selectortools.DivisionSelector(
            inequality=timetools.TimespanInequality(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=timetools.SingleSourceSymbolicTimespan(
                    selector=selectortools.SingleSegmentSelector(
                        identifier='red'
                        )
                    )
                )
            )

    Select the last two divisions that start during segment ``'red'``::

        >>> division_selector = selectortools.DivisionSelector(inequality=inequality, start_identifier=-2)

    ::

        >>> z(division_selector)
        selectortools.DivisionSelector(
            inequality=timetools.TimespanInequality(
                'timespan_1.start <= timespan_2.start < timespan_1.stop',
                timespan_1=timetools.SingleSourceSymbolicTimespan(
                    selector=selectortools.SingleSegmentSelector(
                        identifier='red'
                        )
                    )
                ),
            start_identifier=-2
            )

    Division selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, inequality=None, start_identifier=None, stop_identifier=None):
        SliceSelector.__init__(self, start_identifier=start_identifier, stop_identifier=stop_identifier)
        InequalitySelector.__init__(self, inequality=inequality)
        self._klass = divisiontools.Division

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def klass(self):
        return self._klass

    ### PUBLIC METHODS ###

    def get_score_offsets(self, score_specification, voice_name):
        divisions = self.get_selected_objects(score_specification, voice_name)
        start_offset = divisions[0].start_offset
        stop_offset = divisions[-1].stop_offset
        #self._debug((start_offset, stop_offset), 'offsets')
        return start_offset, stop_offset
        
    def get_score_start_offset(self, score_specification, voice_name):
        r'''Get selector score start offset of selector when selector is applied
        to `voice_name` in `score_specification`.

        .. note:: add example.

        Return offset.
        '''
        start_offset, stop_offset = self.get_score_offsets(score_specification, voice_name)
        return start_offset

    def get_score_stop_offset(self, score_specification, voice_name):
        r'''Get selector score stop offset of selector when selector is applied
        to `voice_name` in `score_specification`.

        Return offset.
        '''
        start_offset, stop_offset = self.get_score_offsets(score_specification, voice_name)
        return stop_offset

    def get_selected_objects(self, score_specification, voice_name):
        '''Get divisions selected when selector is applied
        to `voice_name` in `score_specification`.

        .. note:: add example.
        
        Return list of zero or more offset-positioned divisions.
        '''
        voice_division_list = score_specification.contexts[voice_name]['voice_division_list']
        divisions = []
        for division in voice_division_list:
            if self.inequality is None or self.inequality(timespan_2=division, 
                score_specification=score_specification, context_name=voice_name):
                divisions.append(division)
        divisions = divisions[self.start_identifier:self.stop_identifier]
        return divisions
    
    def set_segment_identifier(self, segment_identifier):
        '''Delegate to ``self.inequality.set_segment_identifier()``.
        '''
        self.inequality.set_segment_identifier(segment_identifier)
