from abjad.tools.abctools import AbjadObject


class _Solver(AbjadObject):

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### PUBLIC PROPERTIES ###

    @property
    def constraints(self):
        return self._constraints

    @property
    def domain(self):
        return self._domain

    @property
    def iterator(self):
        return self.__iter__()

    @property
    def randomized(self):
        return self._randomized

    @property
    def solutions(self):
        return [x for x in self.iterator]

    ### PUBLIC METHODS ###

    def get_le_n_solutions(self, n):
        assert 0 < n
        solutions = []
        iter = self.iterator
        for _ in xrange(n):
            try:
                solutions.append(iter.next( ))
            except StopIteration:
                break
        return tuple(solutions)

