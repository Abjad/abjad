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
            >>> tree = sequencetools.CyclicTree(sequence)

        Get next 4 nodes at level 2:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(4, 2)
            [CyclicTree(1), CyclicTree(2), CyclicTree(3), CyclicTree(4)]

        Get next 10 nodes at level 2:

        ::

            >>> for node in tree[0][0].get_next_n_nodes_at_level(10, 2):
            ...     node
            CyclicTree(1)
            CyclicTree(2)
            CyclicTree(3)
            CyclicTree(4)
            CyclicTree(5)
            CyclicTree(6)
            CyclicTree(7)
            CyclicTree(1)
            CyclicTree(2)
            CyclicTree(3)

        ### PREVIOUS MNODES ###

        Get previous 4 nodes at level 2:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(-4, 2)
            [CyclicTree(7), CyclicTree(6), CyclicTree(5), CyclicTree(4)]

        Get previous 10 nodes at level 2:

        ::

            >>> for node in tree[0][0].get_next_n_nodes_at_level(-10, 2):
            ...     node
            CyclicTree(7)
            CyclicTree(6)
            CyclicTree(5)
            CyclicTree(4)
            CyclicTree(3)
            CyclicTree(2)
            CyclicTree(1)
            CyclicTree(7)
            CyclicTree(6)
            CyclicTree(5)

        Return list of nodes.
        '''
        return Tree.get_next_n_nodes_at_level(self, n, level)

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

    def iterate_forever_depth_first(self, reverse=False):
        '''Iterate tree depth first.

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> cyclic_tree = sequencetools.CyclicTree(sequence)

        Example 1. Iterate from left to right:

        ::

            >>> generator = cyclic_tree.iterate_forever_depth_first()
            >>> for i in range(20):
            ...     generator.next()
            CyclicTree([[0, 1], [2, 3], [4, 5], [6, 7]])
            CyclicTree([0, 1])
            CyclicTree(0)
            CyclicTree(1)
            CyclicTree([2, 3])
            CyclicTree(2)
            CyclicTree(3)
            CyclicTree([4, 5])
            CyclicTree(4)
            CyclicTree(5)
            CyclicTree([6, 7])
            CyclicTree(6)
            CyclicTree(7)
            CyclicTree([[0, 1], [2, 3], [4, 5], [6, 7]])
            CyclicTree([0, 1])
            CyclicTree(0)
            CyclicTree(1)
            CyclicTree([2, 3])
            CyclicTree(2)
            CyclicTree(3)

        Example 2. Iterate from right to left:

        ::

            >>> generator = cyclic_tree.iterate_forever_depth_first(reverse=True)
            >>> for i in range(20):
            ...     generator.next()
            CyclicTree([[0, 1], [2, 3], [4, 5], [6, 7]])
            CyclicTree([6, 7])
            CyclicTree(7)
            CyclicTree(6)
            CyclicTree([4, 5])
            CyclicTree(5)
            CyclicTree(4)
            CyclicTree([2, 3])
            CyclicTree(3)
            CyclicTree(2)
            CyclicTree([0, 1])
            CyclicTree(1)
            CyclicTree(0)
            CyclicTree([[0, 1], [2, 3], [4, 5], [6, 7]])
            CyclicTree([6, 7])
            CyclicTree(7)
            CyclicTree(6)
            CyclicTree([4, 5])
            CyclicTree(5)
            CyclicTree(4)

        Return node generator.
        '''
        while True:
            for node in Tree.iterate_depth_first(self, reverse=reverse):
                yield node
