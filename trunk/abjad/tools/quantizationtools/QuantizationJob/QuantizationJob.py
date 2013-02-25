import inspect
from abjad.tools.abctools import AbjadObject


class QuantizationJob(AbjadObject):
    '''A copiable, picklable class for generating all ``QGrids`` which are valid
    under a given ``SearchTree`` for a sequence of ``QEventProxies``:

    ::

        >>> q_event_a = quantizationtools.PitchedQEvent(250, [0, 1])
        >>> q_event_b = quantizationtools.SilentQEvent(500)
        >>> q_event_c = quantizationtools.PitchedQEvent(750, [3, 7])
        >>> proxy_a = quantizationtools.QEventProxy(q_event_a, 0.25)
        >>> proxy_b = quantizationtools.QEventProxy(q_event_b, 0.5)
        >>> proxy_c = quantizationtools.QEventProxy(q_event_c, 0.75)

    ::

        >>> definition = {2: {2: None}, 3: None, 5: None}
        >>> search_tree = quantizationtools.UnweightedSearchTree(definition)

    ::

        >>> job = quantizationtools.QuantizationJob(
        ...     1, search_tree, [proxy_a, proxy_b, proxy_c])

    ``QuantizationJob`` generates ``QGrids`` when called, and stores those
    ``QGrids`` on its ``q_grids`` attribute, allowing them to be recalled later,
    even if pickled:

    ::

        >>> job()
        >>> for q_grid in job.q_grids:
        ...     print q_grid.rtm_format
        1
        (1 (1 1 1 1 1))
        (1 (1 1 1))
        (1 (1 1))
        (1 ((1 (1 1)) (1 (1 1))))

    ``QuantizationJob`` is intended to be useful in multiprocessing-enabled environments.

    Return ``QuantizationJob`` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_job_id', '_q_event_proxies', '_q_grids', '_search_tree')

    ### INITIALIZER ###

    def __init__(self, job_id, search_tree, q_event_proxies, q_grids=None):
        from abjad.tools import quantizationtools

        assert isinstance(search_tree, quantizationtools.SearchTree)
        assert all([isinstance(x, quantizationtools.QEventProxy) for x in q_event_proxies])
        self._job_id = job_id
        self._search_tree = search_tree
        self._q_event_proxies = tuple(q_event_proxies)
        if q_grids is None:
            self._q_grids = ()
        else:
            assert all([isinstance(x, quantizationtools.QGrid) for x in q_grids])
            self._q_grids = tuple(q_grids)

    ### SPECIAL METHODS ###

    def __call__(self):
        from abjad.tools import quantizationtools
        q_grid = quantizationtools.QGrid()
        q_grid.fit_q_events(self.q_event_proxies)
        old_q_grids = []
        new_q_grids = [q_grid]
        while new_q_grids:
            q_grid = new_q_grids.pop()
            new_q_grids.extend(self.search_tree(q_grid))
            old_q_grids.append(q_grid)
        self._q_grids = tuple(old_q_grids)

    def __eq__(self, expr):
        if type(self) == type(expr):
            if self.job_id == expr.job_id:
                if self.search_tree == expr.search_tree:
                    if self.q_event_proxies == expr.q_event_proxies:
                        if self.q_grids == expr.q_grids:
                            return True
        return False

    def __getnewargs__(self):
        return (self.job_id, self.search_tree, self.q_event_proxies, self.q_grids)

    def __getstate__(self):
        return {
            '_job_id': self.job_id,
            '_q_event_proxies': self.q_event_proxies,
            '_q_grids': self.q_grids,
            '_search_tree': self.search_tree,
        }

    def __setstate__(self, state):
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def job_id(self):
        '''The job id of the ``QuantizationJob``:

        ::

            >>> job.job_id
            1

        Only meaningful when the job is processed via multiprocessing,
        as the job id is necessary to reconstruct the order of jobs.

        Return int.
        '''
        return self._job_id

    @property
    def q_event_proxies(self):
        '''The ``QEventProxies`` the ``QuantizationJob`` was instantiated with:

        ::

            >>> for q_event_proxy in job.q_event_proxies:
            ...     q_event_proxy
            quantizationtools.QEventProxy(
                quantizationtools.PitchedQEvent(
                    durationtools.Offset(250, 1),
                    (NamedChromaticPitch("c'"), NamedChromaticPitch("cs'")),
                    attachments=()
                    ),
                durationtools.Offset(1, 4)
                )
            quantizationtools.QEventProxy(
                quantizationtools.SilentQEvent(
                    durationtools.Offset(500, 1),
                    attachments=()
                    ),
                durationtools.Offset(1, 2)
                )
            quantizationtools.QEventProxy(
                quantizationtools.PitchedQEvent(
                    durationtools.Offset(750, 1),
                    (NamedChromaticPitch("ef'"), NamedChromaticPitch("g'")),
                    attachments=()
                    ),
                durationtools.Offset(3, 4)
                )

        Return tuple.
        '''
        return self._q_event_proxies

    @property
    def q_grids(self):
        '''The generated ``QGrids``:

        ::

            >>> for q_grid in job.q_grids:
            ...     print q_grid.rtm_format
            1
            (1 (1 1 1 1 1))
            (1 (1 1 1))
            (1 (1 1))
            (1 ((1 (1 1)) (1 (1 1))))

        Return tuple.
        '''
        return self._q_grids

    @property
    def search_tree(self):
        '''The search tree the ``QuantizationJob`` was instantiated with:

        ::

            >>> job.search_tree
            UnweightedSearchTree(
                definition={   2: {   2: None}, 3: None, 5: None}
                )

        Return ``SearchTree`` instance.
        '''
        return self._search_tree

