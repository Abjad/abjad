from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import sequencetools
from abjad.tools import timespantools
from experimental.tools.selectortools.Selector import Selector


class BackgroundMeasureSelector(Selector):
    r'''Background measure selector.

    ::

        >>> from experimental.tools import *

    ::

        >>> score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score_specification = specificationtools.ScoreSpecification(score_template=score_template)
        >>> red_segment = score_specification.append_segment(name='red')

    Select voice ``1`` measures that start during score::

        >>> selector = score_specification.interface.select_background_measures('Voice 1')

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSelector(
            voice_name='Voice 1'
            )

    Select voice ``1`` measures starting during segment ``'red'``::

        >>> selector = red_segment.select_background_measures('Voice 1')

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSelector(
            anchor='red',
            voice_name='Voice 1'
            )

    Select voice ``1`` measures that start during three contiguous segments::

        >>> segments = score_specification.interface.select_segments('Voice 1')['red':('red', 3)]
        >>> selector = segments.select_background_measures('Voice 1')

    ::

        >>> z(selector)
        selectortools.BackgroundMeasureSelector(
            anchor=selectortools.SegmentSelector(
                voice_name='Voice 1',
                request_modifiers=settingtools.ModifierInventory([
                    "result = self.___getitem__(elements, start_offset, slice('red', ('red', 3), None))"
                    ])
                ),
            voice_name='Voice 1'
            )

    Background measure selectors are immutable.
    '''

    ### PRIVATE METHODS ###

    # using during time signature interpretation before segment start offsets are calculated
    def _get_time_signatures_without_timespan(self, score_specification, 
        voice_name=None, start_offset=None, stop_offset=None):
        start_segment_specification = score_specification.get_start_segment_specification(self)
        time_signatures = start_segment_specification.time_signatures[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        time_signatures, dummy = self._apply_request_modifiers(time_signatures, None)
        return time_signatures

    def _get_timespan(self, score_specification, context_name):
        timespan, time_signatures = self._get_timespan_and_selected_objects(score_specification, context_name)
        timespan = self._apply_timespan_modifiers(timespan)
        return timespan

    def _get_timespan_and_selected_objects(self, score_specification, context_name):
        start_segment_specification = score_specification.get_start_segment_specification(self)
        time_signatures = start_segment_specification.time_signatures[:]
        time_signatures = [mathtools.NonreducedFraction(x) for x in time_signatures]
        start_offset = start_segment_specification.timespan.start_offset
        time_signatures, start_offset = self._apply_request_modifiers(time_signatures, start_offset)
        duration = sum([durationtools.Duration(x) for x in time_signatures])
        stop_offset = start_offset + duration
        timespan = timespantools.Timespan(start_offset, stop_offset)
        return timespan, time_signatures
