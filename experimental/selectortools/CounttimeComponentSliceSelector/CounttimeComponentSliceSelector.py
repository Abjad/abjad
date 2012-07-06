from experimental.selectortools.Selector import Selector


class CounttimeComponentSliceSelector(Selector):
    r'''.. versionadded:: 1.0

    Select `container` elements from `start` to `stop`.

    Select the first five elements of ``'Voice 1'``::

        >>> from experimental import selectortools
        >>> from experimental import specificationtools

    ::

        >>> voice = selectortools.CounttimeComponentSelector(context='Voice 1')

    ::

        >>> selectortools.CounttimeComponentSliceSelector(voice, stop=5)
        CounttimeComponentSliceSelector(CounttimeComponentSelector(context='Voice 1'), stop=5)

    Select the last five elements of ``'Voice 1'``::

        >>> selectortools.CounttimeComponentSliceSelector(voice, start=-5)
        CounttimeComponentSliceSelector(CounttimeComponentSelector(context='Voice 1'), start=-5)

    Select all elements of  ``'Voice 1'`` between ``5`` and ``-5``::

        >>> selectortools.CounttimeComponentSliceSelector(voice, start=5, stop=-5)
        CounttimeComponentSliceSelector(CounttimeComponentSelector(context='Voice 1'), start=5, stop=-5)

    Select all elements of of ``'Voice 1'``::

        >>> selectortools.CounttimeComponentSliceSelector(voice)
        CounttimeComponentSliceSelector(CounttimeComponentSelector(context='Voice 1'))

    Slice selector interface mirrors Python slice syntax as closely as possible.

    (Though the optional slice stride parameter is not supported.)

    Because of this only integer values and none are allowed as start and stop values.

    Selections of contiguous named objects must be made in another way.
    '''

    ### INITIALIZER ###

    def __init__(self, container, start=None, stop=None):
        from experimental import selectortools
        assert isinstance(container, selectortools.CounttimeComponentSelector), repr(container)
        assert isinstance(start, (int, type(None))), repr(start)
        assert isinstance(stop, (int, type(None))), repr(stop)
        Selector.__init__(self)
        self._container = container
        self._start = start
        self._stop = stop

    ### PUBLIC ATTRIBUTES ###

    @property
    def container(self):
        '''Slice selector container initialized by user.

        Return score object selector.
        '''
        return self._container

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
