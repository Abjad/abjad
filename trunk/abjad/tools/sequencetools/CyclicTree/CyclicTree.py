from abjad.tools.sequencetools.CyclicList import CyclicList
from abjad.tools.sequencetools.Tree import Tree


class CyclicTree(Tree):
    r'''.. versionadded:: 2.5

    Abjad data structure to work with a sequence whose elements have been
    grouped into arbitrarily many levels of cyclic containment.

    Exactly like the ``Tree`` class but with the additional affordance
    that all integer indices of any size work at every level of structure.

    Cyclic trees raise no index errors.

    Here is a cyclic tree:

    ::

        >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
        >>> cyclic_tree = sequencetools.CyclicTree(sequence)

    ::

        >>> cyclic_tree
        CyclicTree([[0, 1], [2, 3], [4, 5], [6, 7]])

    Here's an internal node:

    ::

        >>> cyclic_tree[2]
        CyclicTree([4, 5])

    Here's the same node indexed with a different way:

    ::

        >>> cyclic_tree[2]
        CyclicTree([4, 5])

    With a negative index:

    ::

        >>> cyclic_tree[-2]
        CyclicTree([4, 5])

    And another negative index:

    ::

        >>> cyclic_tree[-6]
        CyclicTree([4, 5])

    Here's a leaf node:

    ::

        >>> cyclic_tree[2][0]
        CyclicTree(4)

    And here's the same node indexed a different way:

    ::

        >>> cyclic_tree[2][20]
        CyclicTree(4)

    All other interface attributes function as in ``Tree``.
    '''

    ### SPECIAL METHODS ###

    def __iter__(self):
        return self._noncyclic_children.__iter__()

    ### PRVATE METHODS ###

    def _initialize_children_list(self):
        return CyclicList([])

    ### PUBLIC METHODS ###

    def get_next_n_nodes_at_level(self, n, level):
        '''Get next `n` nodes at `level`:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        Get next 4 nodes at level 2:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(4, 2)
            [Tree(1), Tree(2), Tree(3), Tree(4)]

        Get next 20 nodes at level 2:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(20, 2) # doctest: +SKIP

        .. note:: make this work.

        Return list of nodes.
        '''
        return Tree.get_next_n_nodes_at_level(n, level)
        
    def get_node_at_position(self, position):
        '''Get node at `position`:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> cyclic_tree = sequencetools.CyclicTree(sequence)

        ::

            >>> cyclic_tree.get_node_at_position((2, 1))
            CyclicTree(5)

        ::

            >>> cyclic_tree.get_node_at_position((2, 99))
            CyclicTree(5)

        ::

            >>> cyclic_tree.get_node_at_position((82, 1))
            CyclicTree(5)

        ::

            >>> cyclic_tree.get_node_at_position((82, 99))
            CyclicTree(5)

        Return node.
        '''
        return Tree.get_node_at_position(self, position)
