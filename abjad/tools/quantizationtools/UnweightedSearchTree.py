# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.quantizationtools.SearchTree import SearchTree


class UnweightedSearchTree(SearchTree):
    r'''Concrete ``SearchTree`` subclass, based on Paul Nauert's search
    tree model:

    ::

        >>> search_tree = quantizationtools.UnweightedSearchTree()
        >>> print(format(search_tree))
        quantizationtools.UnweightedSearchTree(
            definition={
                2: {
                    2: {
                        2: {
                            2: None,
                            },
                        3: None,
                        },
                    3: None,
                    5: None,
                    7: None,
                    },
                3: {
                    2: {
                        2: None,
                        },
                    3: None,
                    5: None,
                    },
                5: {
                    2: None,
                    3: None,
                    },
                7: {
                    2: None,
                    },
                11: None,
                13: None,
                },
            )

    The search tree defines how nodes in a ``QGrid`` may be subdivided,
    if they happen to contain ``QEvents`` (or, in actuality, ``QEventProxy``
    instances which reference ``QEvents``, but rescale their offsets between
    ``0`` and ``1``).

    In the default definition, the root node of the ``QGrid`` may be
    subdivided into ``2``, ``3``, ``5``, ``7``, ``11`` or ``13`` equal parts.
    If divided into ``2`` parts, the divisions of the root node may be
    divided again into ``2``, ``3``, ``5`` or ``7``, and so forth.

    This definition is structured as a collection of nested dictionaries,
    whose keys are integers, and whose values are either the sentinel ``None``
    indicating no further permissable divisions, or dictionaries obeying
    these same rules, which then indicate the possibilities for further
    division.

    Calling a ``UnweightedSearchTree`` with a ``QGrid`` instance will
    generate all permissable subdivided ``QGrids``, according to the
    definition of the called search tree:

    ::

        >>> q_event_a = quantizationtools.PitchedQEvent(130, [0, 1, 4])
        >>> q_event_b = quantizationtools.PitchedQEvent(150, [2, 3, 5])
        >>> proxy_a = quantizationtools.QEventProxy(q_event_a, 0.5)
        >>> proxy_b = quantizationtools.QEventProxy(q_event_b, 0.667)
        >>> q_grid = quantizationtools.QGrid()
        >>> q_grid.fit_q_events([proxy_a, proxy_b])

    ::

        >>> q_grids = search_tree(q_grid)
        >>> for grid in q_grids:
        ...     print(grid.rtm_format)
        (1 (1 1))
        (1 (1 1 1))
        (1 (1 1 1 1 1))
        (1 (1 1 1 1 1 1 1))
        (1 (1 1 1 1 1 1 1 1 1 1 1))
        (1 (1 1 1 1 1 1 1 1 1 1 1 1 1))

    A custom ``UnweightedSearchTree`` may be defined by passing in a
    dictionary, as described above.
    The following search tree only permits divisions of
    the root node into ``2s`` and ``3s``, and if divided into ``2``,
    a node may be divided once more into ``2`` parts:

    ::

        >>> definition = {2: {2: None}, 3: None}
        >>> search_tree = quantizationtools.UnweightedSearchTree(definition)

    ::

        >>> q_grids = search_tree(q_grid)
        >>> for grid in q_grids:
        ...     print(grid.rtm_format)
        (1 (1 1))
        (1 (1 1 1))

    Return ``UnweightedSearchTree`` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PRIVATE METHODS ###

    def _find_leaf_subdivisions(self, parentage_ratios):
        parentage = [x[1] for x in parentage_ratios[1:]]
        if not parentage:
            return tuple((1,) * x for x in sorted(self._definition.keys()))
        node = self._definition[parentage[0]]
        for item in parentage[1:]:
            node = node[item]
            if node is None:
                return ()
        if node is None:
            return ()
        return tuple((1,) * x for x in sorted(node.keys()))

    def _is_valid_definition(self, definition):
        def recurse(n):
            results = []
            for key in n:
                if not isinstance(key, int) or \
                    not 0 < key or \
                    not mathtools.divisors(key) == [1, key]:
                    results.append(False)
                elif not isinstance(n[key], (dict, type(None))):
                    results.append(False)
                elif isinstance(n[key], dict) and not recurse(n[key]):
                    results.append(False)
                else:
                    results.append(True)
            return results
        if not isinstance(definition, dict) or not len(definition):
            return False
        return all(recurse(definition))

    ### PUBLIC PROPERTIES ###

    @property
    def default_definition(self):
        r'''The default search tree definition, based on the search tree given
        by Paul Nauert:

        ::

            >>> import pprint
            >>> search_tree = quantizationtools.UnweightedSearchTree()
            >>> pprint.pprint(search_tree.default_definition)
            {2: {2: {2: {2: None}, 3: None}, 3: None, 5: None, 7: None},
             3: {2: {2: None}, 3: None, 5: None},
             5: {2: None, 3: None},
             7: {2: None},
             11: None,
             13: None}

        Returns dictionary.
        '''
        return {
            2: {                  # 1/2
                2: {              # 1/4
                    2: {          # 1/8
                        2: None,  # 1/16
                        },
                    3: None,      # 1/12
                    },
                3: None,          # 1/6
                5: None,          # 1/10
                7: None,          # 1/14
                },
            3: {                  # 1/3
                2: {              # 1/6
                    2: None,      # 1/12
                    },
                3: None,          # 1/9
                5: None,          # 1/15
                },
            5: {                  # 1/5
                2: None,          # 1/10
                3: None,          # 1/15
                },
            7: {                  # 1/7
                2: None,          # 1/14
                },
            11: None,             # 1/11
            13: None,             # 1/13
            }
