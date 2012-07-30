from abjad.tools import mathtools
from experimental.quantizationtools.SearchTree import SearchTree


class SimpleSearchTree(SearchTree):

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def default_definition(self):
        return {
            2: {                 # 1/2
                2: {             # 1/4
                    2: {         # 1/8
                        2: None, # 1/16
                    },
                    3: None,     # 1/12
                },
                3: None,         # 1/6
                5: None,         # 1/10
                7: None,         # 1/14
            },
            3: {                 # 1/3
                2: {             # 1/6
                    2: None,     # 1/12
                },
                3: None,         # 1/9
                5: None,         # 1/15
            },
            5: {                 # 1/5
                2: None,         # 1/10
                3: None,         # 1/15
            },
            7: {                 # 1/7
                2: None,         # 1/14
            },
            11: None,            # 1/11
            13: None,            # 1/13
        }

    ### PUBLIC METHODS ###

    def find_leaf_subdivisions(self, parentage_ratios):
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

    def is_valid_definition(self, definition):
        if not isinstance(definition, dict) or not len(definition):
            return False
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
        return all(recurse(definition))
