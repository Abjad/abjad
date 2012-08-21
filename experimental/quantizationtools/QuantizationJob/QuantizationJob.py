from abjad.tools import abctools
from experimental.quantizationtools.QEventProxy import QEventProxy
from experimental.quantizationtools.SearchTree import SearchTree
from experimental.quantizationtools.QGrid import QGrid
import inspect


class QuantizationJob(abctools.AbjadObject):
    '''A copible, picklable class for generating all QGrids which are valid
    under a given SearchTree for a sequence of QEventProxies.

    QuantizationJob is intended to be useful in multiprocessing-enabled environments.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_job_id', '_q_event_proxies', '_q_grids', '_search_tree')

    ### INITIALIZER ###

    def __init__(self, job_id, search_tree, q_event_proxies, q_grids=None):
        assert isinstance(search_tree, SearchTree)
        assert all([isinstance(x, QEventProxy) for x in q_event_proxies])
        self._job_id = job_id
        self._search_tree = search_tree
        self._q_event_proxies = tuple(q_event_proxies)
        if q_grids is None:
            self._q_grids = ()
        else:
            assert all([isinstance(x, QGrid) for x in q_grids])
            self._q_grids = tuple(q_grids)

    ### SPECIAL METHODS ###

    def __call__(self):
        q_grid = QGrid()
        q_grid.fit_q_events(self.q_event_proxies)
        old_q_grids = []
        new_q_grids = [q_grid]
        while new_q_grids:
            q_grid = new_q_grids.pop()
            new_q_grids.extend(self.search_tree(q_grid))
            old_q_grids.append(q_grid)
        self._q_grids = tuple(old_q_grids)

    def __eq__(self, other):
        if type(self) == type(other):
            if self.job_id == other.job_id:
                if self.search_tree == other.search_tree:
                    if self.q_event_proxies == other.q_event_proxies:
                        if self.q_grids == other.q_grids:
                            return True
        return False

    def __getnewargs__(self):
        return (self.job_id, self.search_tree, self.q_event_proxies, self.q_grids)

    def __getstate__(self):
        state = {}
        for klass in inspect.getmro(self.__class__):
            if hasattr(klass, '__slots__'):
                for slot in klass.__slots__:
                    if slot not in state:
                        state[slot] = getattr(self, slot)
        return state

    def __setstate__(self, state):
        for key, value in state.iteritems():
            setattr(self, key, value)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def job_id(self):
        return self._job_id

    @property
    def q_event_proxies(self):
        return self._q_event_proxies

    @property
    def q_grids(self):
        return self._q_grids

    @property
    def search_tree(self):
        return self._search_tree

