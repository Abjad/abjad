from abjad.tools.sequencetools.CyclicList import CyclicList
from abjad.tools.sequencetools.Tree import Tree


class CyclicTree(Tree):
    r'''.. versionadded:: 2.5

    Like ``Tree`` but with cyclic s
    Abjad data structure to work with a sequence whose elements have been
    grouped into arbitrarily many levels of **cyclic** containment.

    Exactly like the ``Tree`` class but with the additional affordance
    that all integer indices of any size work at every level of structure;
    like ``CyclicTuple``, ``CyclicList`` and ``CyclicMatrix``,
    no index errors raises in working with objects of this class.

    ::

        abjad> from abjad.tools import sequencetools

    Here is a cyclic tree::

        abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
        abjad> cyclic_tree = sequencetools.CyclicTree(sequence)

    ::

        abjad> cyclic_tree
        CyclicTree([[0, 1], [2, 3], [4, 5], [6, 7]])

    Here's an internal node::

        abjad> cyclic_tree[2]
        CyclicTree([4, 5])

    Here's the same node indexed with a different way::

        abjad> cyclic_tree[2]
        CyclicTree([4, 5])

    With a negative index::

        abjad> cyclic_tree[-2]
        CyclicTree([4, 5])

    And another negative index::

        abjad> cyclic_tree[-6]
        CyclicTree([4, 5])

    Here's a leaf node::

        abjad> cyclic_tree[2][0]
        CyclicTree(4)

    And here's the same node indexed a different way::

        abjad> cyclic_tree[2][20]
        CyclicTree(4)

    All other interface attributes function as in ``Tree``.
    '''

    ### OVERLOADS ###

    def __iter__(self):
        return self._noncyclic_children.__iter__()

    ### PRVATE METHODS ###

    def _initialize_children_list(self):
        return CyclicList([])
