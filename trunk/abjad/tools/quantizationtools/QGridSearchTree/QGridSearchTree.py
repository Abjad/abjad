from copy import deepcopy
from abjad import Fraction
from abjad.core import _Immutable
from abjad.core import _ImmutableDictionary
from abjad.tools.contexttools import TempoMark
from abjad.tools.durationtools import Offset
from abjad.tools.mathtools import divisors
from abjad.tools.quantizationtools.is_valid_beatspan import is_valid_beatspan
from abjad.tools.quantizationtools.tempo_scaled_rational_to_milliseconds \
    import tempo_scaled_rational_to_milliseconds


class QGridSearchTree(_Immutable, _ImmutableDictionary):
    '''A utility class for defining the permissible divisions of a collection
    of :py:class:`~abjad.tools.quantizationtools.QGrid` objects.

    The search tree is defined by a nested dictionary structure, whose keys
    must be prime integers, and whose values must be None (indicating no further
    possible divisions) or another dictionary following the same rules.

    ::

        abjad> from abjad.tools.quantizationtools import QGridSearchTree

    For example, In the following tree, the beat may be divided into 2 or into 5.
    If divided into 2, it may be divided again into 2 or into 3.

    ::

        abjad> search_tree = QGridSearchTree({2: {2: None, 3: None}, 5: None})

    Return a new `QGridSearchTree`.
    '''

    __slots__ = ('_offsets')

    def __new__(klass, definition = None):
        self = dict.__new__(klass)
        if definition is None:
            definition = self._make_standard_search_tree()
        elif not self._is_valid_search_tree_definition(definition):
            raise ValueError('Search tree definition is invalid: check for primes, malformed subtrees.')
        self._init_immutable_dictionary_recursively(definition)
        self._init_offsets(definition)
        return self

    ### OVERLOADS ###

    def __getnewargs__(self):
        return self.definition

    ### PRIVATE METHODS ###

    def _init_immutable_dictionary_recursively(self, definition):
        def recurse(node, i_node):
            for k, v in node.iteritems():
                if v is None:
                    dict.__setitem__(i_node, k, v)
                else:
                    dict.__setitem__(i_node, k, _ImmutableDictionary())
                    recurse(node[k], i_node[k])
        recurse(definition, self)

    def _init_offsets(self, definition):
        def recurse(n, prev_div, prev_offset):
            results = []
            for k in n:
                div = Fraction(1, k) * prev_div
                for i in range(k):
                    results.append(Offset(prev_offset + (i * div)))
                    if n[k] is not None:
                        results.extend(recurse(n[k], div, prev_offset + (i * div)))
            return results
        offsets = list(sorted(set(recurse(definition, 1, 0))))
        offsets.append(Offset(1))
        object.__setattr__(self, '_offsets', tuple(offsets))

    def _is_valid_search_tree_definition(self, definition):
        if not isinstance(definition, dict) or not len(definition):
            return False
        def recurse(n):
            results = []
            for key in n:
                if not isinstance(key, int) or \
                    not 0 < key or \
                    not divisors(key) == [1, key]:
                    results.append(False)
                elif not isinstance(n[key], (dict, type(None))):
                    results.append(False)
                elif isinstance(n[key], dict) and not recurse(n[key]):
                    results.append(False)
                else:
                    results.append(True)
            return results
        return all(recurse(definition))

    def _make_standard_search_tree(self):
        return {
            2: {                 # 1/2
                2: {           # 1/4
                    2: {        # 1/8
                        2: None, # 1/16
                    },
                    3: None,    # 1/12
                },
                3: None,       # 1/6
                5: None,       # 1/10
                7: None,       # 1/14
            },
            3: {                 # 1/3
                2: {           # 1/6
                    2: None,    # 1/12
                },
                3: None,       # 1/9
                5: None,       # 1/15
            },
            5: {                 # 1/5
                2: None,       # 1/10
                3: None,       # 1/15
            },
            7: {                 # 1/7
                2: None,       # 1/14
            },
            11: None,            # 1/11
            13: None,            # 1/13
        }

    ### PUBLIC ATTRIBUTES ###

    @property
    def offsets(self):
        '''An ordered tuple of all :py:class:`~abjad.tools.durationtools.Offset`
        objects which those :py:class:`~abjad.tools.quantizationtools.QGrid`
        objects governed by a specific `QGridSearchTree` can contain.

        ::

            abjad> from abjad.tools.quantizationtools import QGridSearchTree
            abjad> qst = QGridSearchTree({2: {3: None}})
            abjad> qst.offsets
            (Offset(0, 1), Offset(1, 6), Offset(1, 3), Offset(1, 2), Offset(2, 3), Offset(5, 6), Offset(1, 1))

        Returns a tuple.
        '''

        return self._offsets

    ### PUBLIC METHODS ###

    def find_subtree_divisibility(self, parentage):
        '''Given a parentage signature, defining some subtree of a `QGridSearchTree`,
        return a tuple of permitted divisions of that subtree.

        ::

            abjad> from abjad.tools.quantizationtools import QGridSearchTree
            abjad> qst = QGridSearchTree({2: {2: None, 3: {7: None, 11: None}}, 5: None})
            abjad> qst.find_subtree_divisibility((2,))
            (2, 3)
            abjad> qst.find_subtree_divisibility((2, 2))
            ()
            abjad> qst.find_subtree_divisibility((2, 3))
            (7, 11)
            abjad> qst.find_subtree_divisibility((2, 3, 7))
            ()

        Returns a tuple.
        '''

        node = self[parentage[0]]
        for item in parentage[1:]:
            node = node[item]
            if node is None:
                return tuple([])
        if node is None:
            return tuple([])
        return tuple(sorted(node.keys()))

    def prune(self, beatspan, tempo, threshold):
        '''Prune those subtrees of a `QGridSearchTree` whose divisions in milliseconds,
        given `beatspan` and `tempo`, would be less than `threshold`.

        This allows a composer to specify the maximum speed any quantization
        operation will permit.

        ::

            abjad> from abjad.tools.quantizationtools import QGridSearchTree
            abjad> qst = QGridSearchTree({2: {2: {2: {2: None}}}})
            abjad> beatspan = Fraction(1, 4)
            abjad> tempo = contexttools.TempoMark((1, 4), 60)
            abjad> qst.prune(beatspan, tempo, 100)
            {2: {2: {2: None}}}
            abjad> qst.prune(beatspan, tempo, 200)
            {2: {2: None}}
            abjad> qst.prune(beatspan, tempo, 400)
            {2: None}

        Returns a new `QGridSearchTree`.
        '''

        assert is_valid_beatspan(beatspan)
        assert isinstance(tempo, TempoMark)
        assert 0 < threshold

        def recurse(old_node, prev_div):
            new_node = {}
            for key in old_node:
                div = Fraction(1, key) * prev_div
                dur = tempo_scaled_rational_to_milliseconds(div, tempo)
                if threshold <= dur:
                    if old_node[key] is None:
                        new_node[key] = None
                    else:
                        new_node[key] = recurse(old_node[key], div)
            if not new_node:
                return None
            return new_node

        result = recurse(self, beatspan)
        if result:
            return QGridSearchTree(recurse(self, beatspan))
        return result
