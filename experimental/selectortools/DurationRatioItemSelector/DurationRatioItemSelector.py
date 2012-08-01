from experimental.selectortools.RatioSelector import RatioSelector
from experimental.selectortools.ItemSelector import ItemSelector


class DurationRatioItemSelector(RatioSelector, ItemSelector):
    r'''.. versionadded:: 1.0

    Partition `reference` by ratio of durations. Then select exactly one part.

        >>> from experimental import *

    Select all background measures starting during segment ``'red'`` in ``'Voice 1'``.
    Then partition these measures ``1:1`` by their duration.
    Then select part ``0`` of this partition::

        >>> segment_selector = selectortools.SegmentItemSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> background_measure_selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> duration_ratio_item_selector = selectortools.DurationRatioItemSelector(
        ... background_measure_selector, (1, 1), index=0)

    ::

        >>> z(duration_ratio_item_selector)
        selectortools.DurationRatioItemSelector(
            selectortools.BackgroundMeasureSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
                        selector=selectortools.SegmentItemSelector(
                            index='red'
                            )
                        )
                    )
                ),
            mathtools.Ratio(1, 1),
            index=0
            )

    All duration ratio item selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, ratio, index=None):
        RatioSelector.__init__(self, reference, ratio)
        ItemSelector.__init__(self, index=index)
