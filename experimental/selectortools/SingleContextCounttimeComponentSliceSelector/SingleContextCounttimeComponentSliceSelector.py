from abjad.tools import voicetools
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.SliceSelector import SliceSelector


class SingleContextCounttimeComponentSliceSelector(SliceSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

    Select zero or more counttime components in `reference` container
    restricted according to keywords.

        >>> from experimental import *

    Select the first five counttime components in ``'Voice 1'``::

        >>> selectortools.SingleContextCounttimeComponentSliceSelector('Voice 1', stop_identifier=5)
        SingleContextCounttimeComponentSliceSelector('Voice 1', stop_identifier=5)

    Select the last five counttime components in ``'Voice 1'``::

        >>> selectortools.SingleContextCounttimeComponentSliceSelector('Voice 1', start_identifier=-5)
        SingleContextCounttimeComponentSliceSelector('Voice 1', start_identifier=-5)

    Select counttime components from ``5`` up to but not including ``-5`` in ``'Voice 1'``::

        >>> selectortools.SingleContextCounttimeComponentSliceSelector('Voice 1', start_identifier=5, stop_identifier=-5)
        SingleContextCounttimeComponentSliceSelector('Voice 1', start_identifier=5, stop_identifier=-5)

    Select all counttime components in ``'Voice 1'``::

        >>> selectortools.SingleContextCounttimeComponentSliceSelector('Voice 1')
        SingleContextCounttimeComponentSliceSelector('Voice 1')

    Select counttime measure ``3`` to starting during segment ``'red'`` in  ``'Voice 1'``.
    Then select the last three leaves in tuplet ``-1`` in this measure::

        >>> segment_selector = selectortools.SegmentItemSelector(identifier='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)

    ::

        >>> measure_selector = selectortools.SingleContextCounttimeComponentSliceSelector(
        ... 'Voice 1', inequality=inequality, klass=Measure, start_identifier=3, stop_identifier=4)

    ::

        >>> tuplet_selector = selectortools.SingleContextCounttimeComponentSliceSelector(
        ... measure_selector, klass=Tuplet, start_identifier=-1)

    ::

        >>> leaf_slice_selector = selectortools.SingleContextCounttimeComponentSliceSelector(
        ... tuplet_selector, klass=leaftools.Leaf, start_identifier=-3)

    ::

        >>> z(leaf_slice_selector)
        selectortools.SingleContextCounttimeComponentSliceSelector(
            selectortools.SingleContextCounttimeComponentSliceSelector(
                selectortools.SingleContextCounttimeComponentSliceSelector(
                    'Voice 1',
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentItemSelector(
                                identifier='red'
                                )
                            )
                        ),
                    klass=measuretools.Measure,
                    start_identifier=3,
                    stop_identifier=4
                    ),
                klass=tuplettools.Tuplet,
                start_identifier=-1
                ),
            klass=leaftools.Leaf,
            start_identifier=-3
            )

    Counttime component slice selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, inequality=None, klass=None, predicate=None, 
        start_identifier=None, stop_identifier=None):
        from experimental import helpertools
        from experimental import selectortools
        assert self._interprets_as_sliceable_selector(reference), repr(reference)
        assert klass is None or helpertools.is_counttime_component_klass_expr(klass), repr(klass)
        assert isinstance(predicate, (helpertools.Callback, type(None))), repr(predicate)
        SliceSelector.__init__(self, start_identifier=start_identifier, stop_identifier=stop_identifier)
        InequalitySelector.__init__(self, inequality=inequality)
        self._reference = self._reference_to_storable_form(reference)
        self._inequality = inequality
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass
        self._predicate = predicate

    ### READ-ONLY PUBLIC ATTRIBUTES ###

    @property
    def context_name(self):
        '''Return string.
        '''
        return self._voice

    @property
    def context_names(self):
        '''Return length-``1`` string.
        '''
        return [self.context_name]

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
