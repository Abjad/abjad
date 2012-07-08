from abc import ABCMeta
from abc import abstractmethod
from experimental.selectortools.SliceSelector import SliceSelector


class BackgroundElementSliceSelector(SliceSelector):
    r'''.. versionadded:: 1.0

    Select zero or more contiguous background elements.
    '''

    ### INITIALIZER ###

    @abstractmethod
    def __init__(self, klass, inequality=None, start=None, stop=None):
        from experimental import specificationtools
        from experimental import timespantools
        assert specificationtools.is_background_element_klass(klass), repr(klass)
        assert isinstance(inequality, (timespantools.TimespanInequality, type(None))), repr(inequality)
        SliceSelector.__init__(self, start=start, stop=stop)
        self._klass = klass
        self._inequality = inequality

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def inequality(self):
        '''Background element slice selector timespan inequality.

        Return timespan inequality or none.
        '''
        return self._inequality

    @property
    def klass(self):
        '''Background element class initialized by user.

        Return class.
        '''
        return self._klass

    @property
    def start(self):
        '''Background element slice selector start.

        Return integer, string, held expression or none.
        '''
        return self._start

    @property
    def stop(self):
        '''Background element slice selector stop.

        Return integer, string, held expression or none.
        '''
        return self._stop
