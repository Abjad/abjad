from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools import mathtools
from abjad.tools import voicetools
from experimental.divisiontools.Division import Division
from experimental.selectortools.InequalitySelector import InequalitySelector
from experimental.selectortools.ItemSelector import ItemSelector
import types


class SingleContextCounttimeComponentSelector(ItemSelector, InequalitySelector):
    r'''.. versionadded:: 1.0

        >>> from experimental import *

    Select ``'Voice 1'`` counttime measure ``3``::

        >>> measure_selector = selectortools.SingleContextCounttimeComponentSelector(
        ... 'Voice 1', klass=Measure, index=3)

    ::

        >>> z(measure_selector)
        selectortools.SingleContextCounttimeComponentSelector(
            'Voice 1',
            klass=measuretools.Measure,
            index=3
            )

    Select ``'Voice 1'`` counttime measure ``3`` starting during segment ``'red'``::

        >>> segment_selector = selectortools.SegmentSelector(index='red')
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=segment_selector.timespan)

    ::

        >>> measure_selector = selectortools.SingleContextCounttimeComponentSelector(
        ... 'Voice 1', inequality=inequality, klass=Measure, index=3)

    ::

        >>> z(measure_selector)
        selectortools.SingleContextCounttimeComponentSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            klass=measuretools.Measure,
            index=3
            )

    Select ``'Voice 1'`` counttime measure ``3`` to start during segment ``'red'``.
    Then select tuplet ``-1`` in this measure::

        >>> tuplet_selector = selectortools.SingleContextCounttimeComponentSelector(
        ... measure_selector, klass=Tuplet, index=-1)

    ::

        >>> z(tuplet_selector)
        selectortools.SingleContextCounttimeComponentSelector(
            selectortools.SingleContextCounttimeComponentSelector(
                'Voice 1',
                inequality=timespantools.TimespanInequality(
                    timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                    timespantools.SingleSourceTimespan(
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

    Select ``'Voice 1'`` counttime measure ``3`` to start during segment ``'red'``.
    Then select note ``0`` in tuplet ``-1`` in this measure::

        >>> note_selector = selectortools.SingleContextCounttimeComponentSelector(
        ... tuplet_selector, klass=Note, index=0) 

    ::

        >>> z(note_selector)
        selectortools.SingleContextCounttimeComponentSelector(
            selectortools.SingleContextCounttimeComponentSelector(
                selectortools.SingleContextCounttimeComponentSelector(
                    'Voice 1',
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
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
            klass=notetools.Note,
            index=0
            )

    Select ``'Voice 1'`` note ``3``::

        >>> note_selector = selectortools.SingleContextCounttimeComponentSelector(
        ... 'Voice 1', klass=Note, index=3)

    ::

        >>> z(note_selector)
        selectortools.SingleContextCounttimeComponentSelector(
            'Voice 1',
            klass=notetools.Note,
            index=3
            )

    Select ``'Voice 1'`` note ``3`` to start during segment ``'red'``::

        >>> selector = selectortools.SingleContextCounttimeComponentSelector(
        ... 'Voice 1', inequality=inequality, klass=Note, index=3)

    ::

        >>> z(selector)
        selectortools.SingleContextCounttimeComponentSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            klass=notetools.Note,
            index=3
            )

    Select ``'Voice 1'`` chord ``20`` with at least six pitches
    to start during segment ``'red'``::

        >>> command = 'lambda x: 6 <= len(x)'
        >>> predicate = helpertools.Callback(eval(command), command)

    ::

        >>> selector = selectortools.SingleContextCounttimeComponentSelector(
        ... 'Voice 1', inequality=inequality, klass=Chord, predicate=predicate, index=20)

    ::

        >>> z(selector)
        selectortools.SingleContextCounttimeComponentSelector(
            'Voice 1',
            inequality=timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.SingleSourceTimespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                ),
            klass=chordtools.Chord,
            predicate=helpertools.Callback('lambda x: 6 <= len(x)'),
            index=20
            )

    Counttime component selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, reference, inequality=None, klass=None, predicate=None, index=None):
        from experimental import helpertools
        from experimental import selectortools
        assert self._interprets_as_sliceable_selector(reference), repr(reference)
        assert klass is None or helpertools.is_counttime_component_klass_expr(klass), repr(klass)
        assert isinstance(predicate, (helpertools.Callback, type(None))), repr(predicate)
        ItemSelector.__init__(self, index=index)
        InequalitySelector.__init__(self, inequality=inequality)
        self._reference = self._reference_to_storable_form(reference)
        if isinstance(klass, tuple):
            klass = helpertools.KlassInventory(klass)
        self._klass = klass
        self._predicate = predicate
    
    ### SPECIAL METHODS ###

    def __eq__(self, other):
        '''True when `other` is a counttime component selector with
        public properties equal to those of `self`.
        
        Otherwise false.
        
        Return boolean.
        '''
        if not isinstance(other, type(self)):
            return False
        elif not self.reference == other.reference:
            return False
        elif not self.inequality == other.inequality:
            return False
        elif not self.klass == other.klass:
            return False
        elif not self.predicate == other.predicate:
            return False
        elif not self.index == other.index:
            return False
        else:
            return True

    ### READ-ONLY PUBLIC PROPERTIES ###
    
    @property
    def context_name(self):
        '''Return string.
        '''
        return self._voice

    @property
    def context_names(self):
        '''Return length-``1`` list.
        '''
        return [self.context_name]

    @property
    def index(self):
        '''Index of counttime component selector specified by user::

            >>> selector.index
            20

        Return integer or none.
        '''
        return self._index

    @property
    def klass(self):
        '''Class of counttime component selector specified by user::

            >>> selector.klass is Chord
            True

        Return counttime component class or none.
        '''
        return self._klass

    @property
    def predicate(self):
        '''Predicate of counttime component selector specified by user::

            >>> selector.predicate
            Callback('lambda x: 6 <= len(x)')

        Return callback or none.
        '''
        return self._predicate

    @property
    def reference(self):
        '''Reference container of counttime component selector specified by user::

            >>> selector.reference
            'Voice 1'

        Return voice name or counttime container selector.
        '''
        return self._reference

    @property
    def start(self):
        '''Leftmost timepoint of counttime component::

            >>> z(selector.start)
            timespantools.Timepoint(
                anchor=selectortools.SingleContextCounttimeComponentSelector(
                    'Voice 1',
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    klass=chordtools.Chord,
                    predicate=helpertools.Callback('lambda x: 6 <= len(x)'),
                    index=20
                    ),
                edge=Left
                )

        Return timepoint.
        '''
        from experimental import timespantools
        return timespantools.Timepoint(anchor=self, edge=Left)

    @property
    def stop(self):
        '''Rightmost timepoint of counttime component::

            >>> z(selector.stop)
            timespantools.Timepoint(
                anchor=selectortools.SingleContextCounttimeComponentSelector(
                    'Voice 1',
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    klass=chordtools.Chord,
                    predicate=helpertools.Callback('lambda x: 6 <= len(x)'),
                    index=20
                    ),
                edge=Right
                )

        Return timepoint.
        '''
        from experimental import timespantools
        return timespantools.Timepoint(anchor=self, edge=Right)

    @property
    def timepoints(self):
        '''Start and stop timepoints of score object.

        Return pair.
        '''
        return self.start, self.stop

    @property
    def timespan(self):
        '''SingleSourceTimespan of counttime component::

            >>> z(selector.timespan)
            timespantools.SingleSourceTimespan(
                selector=selectortools.SingleContextCounttimeComponentSelector(
                    'Voice 1',
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.SingleSourceTimespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    klass=chordtools.Chord,
                    predicate=helpertools.Callback('lambda x: 6 <= len(x)'),
                    index=20
                    )
                )

        Return timespan.
        '''
        from experimental import timespantools

        start, stop = self.timepoints
        return timespantools.SingleSourceTimespan(selector=self)
