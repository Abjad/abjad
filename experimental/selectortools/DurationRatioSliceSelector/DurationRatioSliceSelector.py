from experimental.selectortools.RatioSelector import RatioSelector
from experimental.selectortools.SliceSelector import SliceSelector


class DurationRatioSliceSelector(RatioSelector, SliceSelector):
    r'''.. versionadded:: 1.0

    Partition `reference` by ratio of durations. Then select zero or more contiguous parts.

        >>> from experimental import *

    Select all background measures starting during segment ``'red'`` in ``'Voice 1'``.
    Then partition these measures ``1:1:1:1`` by their duration.
    Then select the last two parts of this partition::

        >>> segment_selector = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> background_measure_selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> duration_ratio_slice_selector = selectortools.DurationRatioSliceSelector(
        ... background_measure_selector, (1, 1, 1, 1), start_identifier=-2)

    ::

        >>> z(duration_ratio_slice_selector)
        selectortools.DurationRatioSliceSelector(
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
            mathtools.Ratio(1, 1, 1, 1),
            start_identifier=-2
            )

    All duration-ratio slice selector properties are read-only.
    '''

    ### INTIALIZER ###

    def __init__(self, reference, ratio, start_identifier=None, stop_identifier=None):
        RatioSelector.__init__(self, reference, ratio)
        SliceSelector.__init__(self, start_identifier=start_identifier, stop_identifier=stop_identifier)
