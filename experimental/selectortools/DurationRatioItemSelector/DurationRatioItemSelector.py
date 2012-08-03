from abjad.tools import mathtools
from experimental.selectortools.RatioSelector import RatioSelector


class DurationRatioItemSelector(RatioSelector):
    r'''.. versionadded:: 1.0

    Partition `reference` by ratio of durations. Then select exactly one part.

        >>> from experimental import *

    Select all background measures starting during segment ``'red'`` in ``'Voice 1'``.
    Then partition these measures ``1:1`` by their duration.
    Then select part ``0`` of this partition::

        >>> segment_selector = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> background_measure_selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> duration_ratio_item_selector = selectortools.DurationRatioItemSelector(
        ... background_measure_selector, (1, 1), 0)

    ::

        >>> z(duration_ratio_item_selector)
        selectortools.DurationRatioItemSelector(
            selectortools.BackgroundMeasureSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            identifier='red'
                            )
                        )
                    )
                ),
            mathtools.Ratio(1, 1),
            0
            )

    All duration ratio item selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, ratio, part):
        RatioSelector.__init__(self, reference, ratio)
        self._part = part

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def part(self):
        return self._part

    @property
    def segment_identifier(self):
        '''Return ``self.reference.segment_identifier``.
        '''
        return self.reference.segment_identifier

    ### PUBLIC METHODS ###

    def get_duration(self, score_specification):
        '''Ask reference for reference duration. Then do ratio math on reference duration.
        '''
        reference_duration = self.reference.get_duration(score_specification)
        parts = mathtools.divide_number_by_ratio(reference_duration, self.ratio)
        part = parts[self.part]
        return part
