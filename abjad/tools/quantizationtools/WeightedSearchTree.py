# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.quantizationtools.SearchTree import SearchTree


class WeightedSearchTree(SearchTree):
    r'''A search tree that allows for dividing nodes in a ``QGrid`` into
    parts with unequal weights:

    ::

        >>> search_tree = quantizationtools.WeightedSearchTree()

    ::

        >>> print(format(search_tree))
        quantizationtools.WeightedSearchTree(
            definition={
                'divisors': (2, 3, 5, 7),
                'max_depth': 3,
                'max_divisions': 2,
                },
            )

    In ``WeightedSearchTree``'s definition:

        * ``divisors`` controls the sum of the parts of the ratio a node
          may be divided into,
        * ``max_depth`` controls how many levels of tuplet nesting
          are permitted, and
        * ``max_divisions`` controls the maximum permitted length of the
          weights in the ratio.

    Thus, the default ``WeightedSearchTree`` permits the following ratios:

    ::

        >>> for x in search_tree.all_compositions:
        ...     x
        ...
        (1, 1)
        (2, 1)
        (1, 2)
        (4, 1)
        (3, 2)
        (2, 3)
        (1, 4)
        (6, 1)
        (5, 2)
        (4, 3)
        (3, 4)
        (2, 5)
        (1, 6)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_all_compositions',
        '_compositions',
        '_definition',
        )

    ### INITIALIZER ###

    def __init__(self, definition=None):
        SearchTree.__init__(self, definition)
        self._compositions = self._precompute_compositions()
        all_compositions = []
        for value in list(self._compositions.values()):
            all_compositions.extend(value)
        self._all_compositions = tuple(all_compositions)

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
        elif not all(isinstance(x, int) and
            1 < x for x in definition['divisors']):
            return False
        elif not all(mathtools.divisors(x) == [1, x]
            for x in definition['divisors']):
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
            compositions[divisor] = [tuple(x) for x in
                mathtools.yield_all_compositions_of_integer(divisor)
                if 1 < len(x) <= max_divisions]
        return compositions

    ### PUBLIC PROPERTIES ###

    @property
    def all_compositions(self):
        r'''All compositions of weighted search tree.
        '''
        return self._all_compositions

    @property
    def default_definition(self):
        r'''Default definition of weighted search tree.

        Returns dictionary.
        '''
        return {
            'divisors': (2, 3, 5, 7),
            'max_depth': 3,
            'max_divisions': 2,
            }
