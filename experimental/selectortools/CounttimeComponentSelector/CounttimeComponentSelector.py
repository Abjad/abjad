from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools import mathtools
from abjad.tools import voicetools
from experimental.specificationtools.Callback import Callback
from experimental.specificationtools.Division import Division
from experimental.specificationtools.SegmentSpecification import SegmentSpecification
from experimental.selectortools.Selector import Selector
import types


class CounttimeComponentSelector(Selector):
    r'''.. versionadded:: 1.0


    Select ``'Voice 1'`` measure ``3`` to start during segment ``'red'``::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    ::

        >>> timespan = selectortools.SegmentSelector(index='red').timespan
        >>> inequality = timespantools.expr_starts_during_timespan(timespan=timespan)

    ::

        >>> selector = selectortools.CounttimeComponentSelector(
        ... 'Voice 1', inequality=inequality, klass=Measure, index=3)

    ::

        >>> z(selector)
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
            )
    
    Select ``'Voice 1'`` note ``3`` to start during segment ``'red'``::

        >>> selector = selectortools.CounttimeComponentSelector(
        ... 'Voice 1', inequality=inequality, klass=Note, index=3)

    ::

        >>> z(selector)
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
            klass=notetools.Note,
            index=3
            )

    Select ``'Voice 1'`` chord ``20`` with at least six pitches
    to start during segment ``'red'``::

        >>> from experimental.specificationtools.Callback import Callback

    ::

        >>> command = 'lambda x: 6 <= len(x)'
        >>> predicate = Callback(eval(command), command)

    ::

        >>> selector = selectortools.CounttimeComponentSelector(
        ... 'Voice 1', inequality=inequality, klass=Chord, predicate=predicate, index=20)

    ::

        >>> z(selector)
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
            klass=chordtools.Chord,
            predicate=specificationtools.Callback('lambda x: 6 <= len(x)'),
            index=20
            )

    Counttime component selectors are immutable.
    '''

    ### INITIALIZER ###

    def __init__(self, container, inequality=None, klass=None, predicate=None, index=None):
        from experimental import specificationtools
        from experimental import timespantools
        assert self._is_counttime_component_selector_reference(container), repr(container)
        assert isinstance(inequality, (timespantools.TimespanInequality, type(None))), repr(inequality)
        assert klass is None or specificationtools.is_counttime_component_klass(klass), repr(klass)
        assert isinstance(predicate, (Callback, type(None))), repr(predicate)
        assert isinstance(index, (int, type(None))), repr(index)
        Selector.__init__(self)
        self._container = specificationtools.expr_to_component_name(container)
        self._inequality = inequality
        self._klass = klass
        self._predicate = predicate
        self._index = index
    
    ### SPECIAL METHODS ###

    def __eq__(self, other):
        '''True when `other` is a counttime component selector with
        public properties equal to those of `self`.
        
        Otherwise false.
        
        Return boolean.
        '''
        if not isinstance(other, type(self)):
            return False
        elif not self.container == other.container:
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

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _one_line_format(self):
        values = [str(x) for x in self._keyword_argument_values if x is not None]
        values = ', '.join(values)
        values = '[{}]'.format(values)
        return values

    ### PRIVATE METHODS ###

    def _is_counttime_component_selector_reference(self, expr):
        '''True if `expr` can serve as reference for self.
        '''
        from experimental import selectortools
        return isinstance(expr, (voicetools.Voice, selectortools.CounttimeComponentSelector, str))

    ### READ-ONLY PUBLIC PROPERTIES ###
    
    @property
    def container(self):
        '''Container of counttime component selector specified by user::

            >>> selector.container
            'Voice 1'

        Return string or other counttime component selector.
        '''
        return self._container

    @property
    def index(self):
        '''Index of counttime component selector specified by user::

            >>> selector.index
            20

        Return integer or none.
        '''
        return self._index

    @property
    def inequality(self):
        '''Timespan inequality of counttime component selector specified by user::

            >>> z(selector.inequality)
            timespantools.TimespanInequality(
                timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                timespantools.Timespan(
                    selector=selectortools.SegmentSelector(
                        index='red'
                        )
                    )
                )

        Return timespan inequality or none.
        '''
        return self._inequality

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

#    @property
#    def segment(self):
#        '''Name of counttime component selector segment specified by user::
#
#            >>> selector.segment
#            'red'
#
#        Return string or none.
#        '''
#        return self._segment

    @property
    def start(self):
        '''Leftmost timepoint of counttime component::

            >>> z(selector.start)
            timespantools.Timepoint(
                anchor=selectortools.CounttimeComponentSelector(
                    'Voice 1',
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.Timespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    klass=chordtools.Chord,
                    predicate=specificationtools.Callback('lambda x: 6 <= len(x)'),
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
                anchor=selectortools.CounttimeComponentSelector(
                    'Voice 1',
                    inequality=timespantools.TimespanInequality(
                        timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                        timespantools.Timespan(
                            selector=selectortools.SegmentSelector(
                                index='red'
                                )
                            )
                        ),
                    klass=chordtools.Chord,
                    predicate=specificationtools.Callback('lambda x: 6 <= len(x)'),
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
        '''Timespan of counttime component::

            >>> z(selector.timespan)
            timespantools.Timespan(
                start=timespantools.Timepoint(
                    anchor=selectortools.CounttimeComponentSelector(
                        'Voice 1',
                        inequality=timespantools.TimespanInequality(
                            timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                            timespantools.Timespan(
                                selector=selectortools.SegmentSelector(
                                    index='red'
                                    )
                                )
                            ),
                        klass=chordtools.Chord,
                        predicate=specificationtools.Callback('lambda x: 6 <= len(x)'),
                        index=20
                        ),
                    edge=Left
                    ),
                stop=timespantools.Timepoint(
                    anchor=selectortools.CounttimeComponentSelector(
                        'Voice 1',
                        inequality=timespantools.TimespanInequality(
                            timespantools.TimespanInequalityTemplate('t.start <= expr.start < t.stop'),
                            timespantools.Timespan(
                                selector=selectortools.SegmentSelector(
                                    index='red'
                                    )
                                )
                            ),
                        klass=chordtools.Chord,
                        predicate=specificationtools.Callback('lambda x: 6 <= len(x)'),
                        index=20
                        ),
                    edge=Right
                    )
                )

        Return timespan.
        '''
        from experimental import timespantools

        start, stop = self.timepoints
        return timespantools.Timespan(start=start, stop=stop)
