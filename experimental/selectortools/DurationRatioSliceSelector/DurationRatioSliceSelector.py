from experimental.selectortools.RatioSelector import RatioSelector


class DurationRatioSliceSelector(RatioSelector):
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
        ... background_measure_selector, (1, 1, 1, 1), start_part=-2)

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
            start_part=-2
            )

    All duration-ratio slice selector properties are read-only.
    '''

    ### INTIALIZER ###

    def __init__(self, reference, ratio, start_part=None, stop_part=None):
        RatioSelector.__init__(self, reference, ratio)
        self._start_part = start_part
        self._stop_part = stop_part

    ### PUBLIC READ-ONLY PROPERTIES ###

    @property
    def start_part(self):
        return self._start_part

    @property
    def stop_part(self):
        return self._stop_part
