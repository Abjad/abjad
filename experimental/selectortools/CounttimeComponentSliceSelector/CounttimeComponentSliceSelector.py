from abjad.tools import voicetools
from experimental.specificationtools.Callback import Callback
from experimental.selectortools.Selector import Selector


class CounttimeComponentSliceSelector(Selector):
    r'''.. versionadded:: 1.0

    Select the first five ``'Voice 1'`` counttime components::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools
        >>> from experimental import timespantools

    ::

        >>> selectortools.CounttimeComponentSliceSelector('Voice 1', stop=5)
        CounttimeComponentSliceSelector('Voice 1', stop=5)

    Select the last five ``'Voice 1'`` counttime components::

        >>> selectortools.CounttimeComponentSliceSelector('Voice 1', start=-5)
        CounttimeComponentSliceSelector('Voice 1', start=-5)

    Select ``'Voice 1'`` counttime components between ``5`` and ``-5``::

        >>> selectortools.CounttimeComponentSliceSelector('Voice 1', start=5, stop=-5)
        CounttimeComponentSliceSelector('Voice 1', start=5, stop=-5)

    Select all ``'Voice 1'`` counttime components::

        >>> selectortools.CounttimeComponentSliceSelector('Voice 1')
        CounttimeComponentSliceSelector('Voice 1')

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
