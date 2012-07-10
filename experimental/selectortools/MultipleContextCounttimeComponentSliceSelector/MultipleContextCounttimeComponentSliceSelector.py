from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class MultipleContextCounttimeComponentSliceSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    ::

        >>> from experimental import selectortools
        >>> from experimental import timespantools

    Select the first ``40`` leaves starting in segment ``'red'``.
    Do this in both ``'Voice 1'`` and ``'Voice 3'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(segment_selector.timespan)
        >>> selector = selectortools.MultipleContextCounttimeComponentSliceSelector(
        ... contexts=['Voice 1', 'Voice 3'], inequality=inequality, klass=leaftools.Leaf, stop=40)

    ::

        >>> z(selector)
        selectortools.MultipleContextCounttimeComponentSliceSelector(
            contexts=['Voice 1', 'Voice 3'],
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            klass=leaftools.Leaf,
            stop=40
            )

    Multiple context counttime component slice selector properties are read-only.
    '''

    ### INITIALIZER ##

    def __init__(self, contexts=None, inequality=None, klass=None, predicate=None, start=None, stop=None):
        from experimental import selectortools
        from experimental import specificationtools
        assert klass is None or selectortools.is_counttime_component_klass_expr(klass), repr(klass)
        assert isinstance(predicate, (specificationtools.Callback, type(None))), repr(predicate)
        SliceSelector.__init__(self, start=start, stop=stop)
        InequalitySelector.__init__(self, inequality=inequality)
        self._contexts = contexts
        self._klass = klass
        self._predicate = predicate

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def contexts(self):
        return self._contexts

    @property
    def klass(self):
        return self._klass

    @property
    def predicate(self):
        return self._predicate
