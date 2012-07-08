from abjad.tools import mathtools
from experimental.selectortools.CountRatioSelector import CountRatioSelector
from experimental.selectortools.ItemSelector import ItemSelector


class CountRatioItemSelector(CountRatioSelector, ItemSelector):
    r'''.. versionadded:: 1.0
    
    Partition `reference` by `ratio`. Then select exactly one part.

        >>> from experimental import selectortools
        >>> from experimental import timespantools

    Select all background measures starting during segment ``'red'`` in ``'Voice 1'``.
    Then partition these measures ``1:1`` by their count.
    Then select part ``0`` of this partition::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> background_measure_selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> count_ratio_item_selector = selectortools.CountRatioItemSelector(
        ... background_measure_selector, (1, 1), index=0)

    ::

        >>> z(count_ratio_item_selector)
        selectortools.CountRatioItemSelector(
            selectortools.BackgroundMeasureSliceSelector(
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.Timespan(
                        selector=selectortools.SegmentSelector(
                            index='red'
                            )
                        )
                    )
                ),
            mathtools.Ratio(1, 1),
            index=0
            )

    Count ratio selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, ratio, index=None):
        CountRatioSelector.__init__(self, reference, ratio)
        ItemSelector.__init__(self, index=index)
