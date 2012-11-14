from abjad.tools import mathtools
from experimental.quantizationtools.SearchTree import SearchTree


class ComplexSearchTree(SearchTree):

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_all_compositions', '_compositions', '_definition')

    ### INITIALIZER ###

    def __init__(self, definition=None):
        SearchTree.__init__(self, definition)
        self._compositions = self._precompute_compositions()
        all_compositions = []
        for value in self._compositions.values():
            all_compositions.extend(value)
        self._all_compositions = tuple(all_compositions)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def default_definition(self):
        return {
            'divisors': (2, 3, 5, 7),
            'max_depth': 3,
            'max_divisions': 2,
        }

    ### PRIVATE METHODS ###

    def _find_leaf_subdivisions(self, parentage_ratios):
        if len(parentage_ratios[1:]) < self._definition['max_depth']:
            return self._all_compositions
        return ()

    def _is_valid_definition(self, definition):
        if not isinstance(definition, dict):
            return False
        elif 'divisors' not in definition:
            return False
        elif not len(definition['divisors']):
            return False
        elif not all([isinstance(x, int) and 1 < x for x in definition['divisors']]):
            return False
        elif not all([mathtools.divisors(x) == [1, x] for x in definition['divisors']]):
            return False
        elif 'max_depth' not in definition:
            return False
        elif not isinstance(definition['max_depth'], int):
            return False
        elif not 0 < definition['max_depth']:
            return False
        elif 'max_divisions' not in definition:
            return False
        elif not isinstance(definition['max_divisions'], int):
            return False
        elif not 1 < definition['max_divisions']:
            return False
        return True

    def _precompute_compositions(self):
        compositions = {}
        max_divisions = self._definition['max_divisions']
        for divisor in self._definition['divisors']:
            compositions[divisor] = [tuple(x) for x in mathtools.yield_all_compositions_of_integer(divisor)
                if 1 < len(x) <= max_divisions]
        return compositions

