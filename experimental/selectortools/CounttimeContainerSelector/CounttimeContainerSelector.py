from experimental.selectortools.CounttimeComponentSelector import CounttimeComponentSelector


class CounttimeContainerSelector(CounttimeComponentSelector):
    r'''.. versionadded:: 1.0

    Select one tuplet, counttime measure or other counttime container.

    Select ``'Voice 1'`` counttime measure ``3``::

        >>> from experimental import selectortools 
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    ::

        >>> selectortools.CounttimeContainerSelector('Voice 1', klass=Measure, index=3)
        CounttimeContainerSelector('Voice 1', klass=measuretools.Measure, index=3)

    Select ``'Voice 1'`` counttime measure ``3`` starting in segment ``'red'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)

    ::

        >>> measure_selector = selectortools.CounttimeContainerSelector(
        ... 'Voice 1', inequality=inequality, klass=Measure, index=3)

    ::

        >>> z(measure_selector)
        selectortools.CounttimeContainerSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            klass=measuretools.Measure,
            index=3
            )

    Select the last tuplet in ``'Voice 1'`` measure ``3`` starting in segment ``'red'``::

        >>> tuplet_selector = selectortools.CounttimeContainerSelector(
        ... measure_selector, klass=Tuplet, index=-1)

    ::

        >>> z(tuplet_selector)
        selectortools.CounttimeContainerSelector(
            selectortools.CounttimeContainerSelector(
                'Voice 1',
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.Timespan(
                        selector=selectortools.SegmentSelector(
                            index='red'
                            )
                        )
                    ),
                klass=measuretools.Measure,
                index=3
                ),
            klass=tuplettools.Tuplet,
            index=-1
            )

    Counttime container selectors are immutable.
    '''

    ### INITIALIZER ##

    def __init__(self, reference, inequality=None, klass=None, predicate=None, index=None):
        CounttimeComponentSelector.__init__(self, reference, 
            inequality=inequality, klass=klass, predicate=predicate, index=index)
