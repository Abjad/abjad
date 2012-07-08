from abjad.tools import voicetools
from experimental.specificationtools.Callback import Callback
from experimental.selectortools.Selector import Selector


class CounttimeComponentSliceSelector(Selector):
    r'''.. versionadded:: 1.0

    Select zero or more counttime components in `reference` container
    restricted according to keywords.

        >>> from experimental import selectortools
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    Select the first five counttime components in ``'Voice 1'``::

        >>> selectortools.CounttimeComponentSliceSelector('Voice 1', stop=5)
        CounttimeComponentSliceSelector('Voice 1', stop=5)

    Select the last five counttime components in ``'Voice 1'``::

        >>> selectortools.CounttimeComponentSliceSelector('Voice 1', start=-5)
        CounttimeComponentSliceSelector('Voice 1', start=-5)

    Select counttime components from ``5`` up to but not including ``-5`` in ``'Voice 1'``::

        >>> selectortools.CounttimeComponentSliceSelector('Voice 1', start=5, stop=-5)
        CounttimeComponentSliceSelector('Voice 1', start=5, stop=-5)

    Select all counttime components in ``'Voice 1'``::

        >>> selectortools.CounttimeComponentSliceSelector('Voice 1')
        CounttimeComponentSliceSelector('Voice 1')

    Select counttime measure ``3`` to starting during segment ``'red'`` in  ``'Voice 1'``.
    Then select the last three leaves in tuplet ``-1`` in this measure::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)

    ::

        >>> measure_selector = selectortools.CounttimeComponentSelector(
        ... 'Voice 1', inequality=inequality, klass=Measure, index=3)

    ::

        >>> tuplet_selector = selectortools.CounttimeComponentSelector(
        ... measure_selector, klass=Tuplet, index=-1)

    ::

        >>> leaf_slice_selector = selectortools.CounttimeComponentSliceSelector(
        ... tuplet_selector, klass=leaftools.Leaf, start=-3)

    ::

        >>> z(leaf_slice_selector)
        selectortools.CounttimeComponentSliceSelector(
            selectortools.CounttimeComponentSelector(
                selectortools.CounttimeComponentSelector(
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
                ),
            klass=leaftools.Leaf,
            start=-3
            )

    Counttime component slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, inequality=None, klass=None, predicate=None, start=None, stop=None):
        from experimental import specificationtools
        from experimental import timespantools
        assert self._is_counttime_selector_reference(reference), repr(reference)
        assert isinstance(inequality, (timespantools.TimespanInequality, type(None))), repr(inequality)
        assert klass is None or specificationtools.is_counttime_component_klass(klass), repr(klass)
        assert isinstance(predicate, (Callback, type(None))), repr(predicate)
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        Selector.__init__(self)
        self._reference = self._reference_to_storable_form(reference)
        self._inequality = inequality
        self._klass = klass
        self._predicate = predicate
        self._start = start
        self._stop = stop

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def inequality(self):
        '''Timespan inequality of counttime component selector specified by user.

        Return timespan inequality or none.
        '''
        return self._inequality

    @property
    def klass(self):
        '''Class of counttime component selector specified by user.

        Return counttime component class or none.
        '''
        return self._klass

    @property
    def predicate(self):
        '''Predicate of counttime component selector specified by user.

        Return callback or none.
        '''
        return self._predicate

    @property
    def reference(self):
        '''Reference container of counttime component slice selector specified by user.

        Return voice name or counttime component selector.
        '''
        return self._reference

    @property
    def start(self):
        '''Slice select start initializer by user.

        Return integer or none.
        '''
        return self._start

    @property
    def stop(self):
        '''Slice select stop initializer by user.

        Return integer or none.
        '''
        return self._stop
