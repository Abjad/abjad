from experimental.selectortools.RatioSelector import RatioSelector


class CountRatioItemSelector(RatioSelector):
    r'''.. versionadded:: 1.0
    
    Partition `reference` by `ratio` of counts. Then select exactly one part.

        >>> from experimental import *

    Select all background measures starting during segment ``'red'`` in ``'Voice 1'``.
    Then partition these measures ``1:1`` by their count.
    Then select part ``0`` of this partition::

        >>> segment_selector = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)
        >>> background_measure_selector = selectortools.BackgroundMeasureSliceSelector(inequality=inequality)

    ::

        >>> count_ratio_item_selector = selectortools.CountRatioItemSelector(
        ... background_measure_selector, (1, 1), 0)

    ::

        >>> z(count_ratio_item_selector)
        selectortools.CountRatioItemSelector(
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

    All count ratio item selector properties are read-only.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, ratio, part):
        assert self._interprets_as_sliceable_selector(reference), repr(reference)
        RatioSelector.__init__(self, reference, ratio)
        self._part = part

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def part(self):
        '''Count-ratio item-selector part.

        Return integer.
        '''
        return self._part
