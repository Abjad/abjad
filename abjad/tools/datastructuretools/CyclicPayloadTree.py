# -*- encoding: utf-8 -*-
from abjad.tools.datastructuretools.CyclicList import CyclicList
from abjad.tools.datastructuretools.PayloadTree import PayloadTree


class CyclicPayloadTree(PayloadTree):
    r'''Abjad data structure to work with a sequence whose elements have been
    grouped into arbitrarily many levels of cyclic containment.

    Exactly like the ``PayloadTree`` class but with the additional affordance
    that all integer indices of any size work at every level of structure.

    Cyclic trees raise no index errors.

    Here is a cyclic tree:

    ::

        >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
        >>> cyclic_tree = datastructuretools.CyclicPayloadTree(sequence)

    ::

        >>> cyclic_tree
        CyclicPayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])

    Here's an internal node:

    ::

        >>> cyclic_tree[2]
        CyclicPayloadTree([4, 5])

    Here's the same node indexed with a different way:

    ::

        >>> cyclic_tree[2]
        CyclicPayloadTree([4, 5])

    With a negative index:

    ::

        >>> cyclic_tree[-2]
        CyclicPayloadTree([4, 5])

    And another negative index:

    ::

        >>> cyclic_tree[-6]
        CyclicPayloadTree([4, 5])

    Here's a leaf node:

    ::

        >>> cyclic_tree[2][0]
        CyclicPayloadTree(4)

    And here's the same node indexed a different way:

    ::

        >>> cyclic_tree[2][20]
        CyclicPayloadTree(4)

    All other interface attributes function as in ``PayloadTree``.
    '''

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats cyclic tree.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __iter__(self):
        r'''Iterates cyclic payload tree.

        ::

            >>> for x in cyclic_tree:
            ...     x
            CyclicPayloadTree([0, 1])
            CyclicPayloadTree([2, 3])
            CyclicPayloadTree([4, 5])
            CyclicPayloadTree([6, 7])

        Yields cyclic payload tree nodes.
        '''
        return self._noncyclic_children.__iter__()

    ### PRVATE METHODS ###

    def _initialize_children_list(self):
        return CyclicList([])

    ### PUBLIC METHODS ###

    def get_next_n_nodes_at_level(self, n, level):
        r'''Gets next `n` nodes of cyclic payload tree at `level`.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.CyclicPayloadTree(sequence)

        Gets next 4 nodes at level 2:

        ::

            >>> for x in tree[0][0].get_next_n_nodes_at_level(4, 2):
            ...     x
            CyclicPayloadTree(1)
            CyclicPayloadTree(2)
            CyclicPayloadTree(3)
            CyclicPayloadTree(4)

        Gets next 10 nodes at level 2:

        ::

            >>> for node in tree[0][0].get_next_n_nodes_at_level(10, 2):
            ...     node
            CyclicPayloadTree(1)
            CyclicPayloadTree(2)
            CyclicPayloadTree(3)
            CyclicPayloadTree(4)
            CyclicPayloadTree(5)
            CyclicPayloadTree(6)
            CyclicPayloadTree(7)
            CyclicPayloadTree(1)
            CyclicPayloadTree(2)
            CyclicPayloadTree(3)

        ### PREVIOUS MNODES ###

        Gets previous 4 nodes at level 2:

        ::

            >>> for x in tree[0][0].get_next_n_nodes_at_level(-4, 2):
            ...     x
            CyclicPayloadTree(7)
            CyclicPayloadTree(6)
            CyclicPayloadTree(5)
            CyclicPayloadTree(4)

        Gets previous 10 nodes at level 2:

        ::

            >>> for node in tree[0][0].get_next_n_nodes_at_level(-10, 2):
            ...     node
            CyclicPayloadTree(7)
            CyclicPayloadTree(6)
            CyclicPayloadTree(5)
            CyclicPayloadTree(4)
            CyclicPayloadTree(3)
            CyclicPayloadTree(2)
            CyclicPayloadTree(1)
            CyclicPayloadTree(7)
            CyclicPayloadTree(6)
            CyclicPayloadTree(5)

        Returns list of nodes.
        '''
        return PayloadTree.get_next_n_nodes_at_level(self, n, level)

    def get_node_at_position(self, position):
        r'''Gets cyclic payload tree node at `position`.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> cyclic_tree = datastructuretools.CyclicPayloadTree(sequence)

        ::

            >>> cyclic_tree.get_node_at_position((2, 1))
            CyclicPayloadTree(5)

        ::

            >>> cyclic_tree.get_node_at_position((2, 99))
            CyclicPayloadTree(5)

        ::

            >>> cyclic_tree.get_node_at_position((82, 1))
            CyclicPayloadTree(5)

        ::

            >>> cyclic_tree.get_node_at_position((82, 99))
            CyclicPayloadTree(5)

        Returns node.
        '''
        return PayloadTree.get_node_at_position(self, position)

    def iterate_forever_depth_first(self, reverse=False):
        r'''Iterate cyclic payload tree tree depth first.

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> cyclic_tree = datastructuretools.CyclicPayloadTree(sequence)

        ..  container:: example
        
            **Example 1.** Iterates from left to right:

            ::

                >>> generator = cyclic_tree.iterate_forever_depth_first()
                >>> for i in range(20):
                ...     generator.next()
                CyclicPayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])
                CyclicPayloadTree([0, 1])
                CyclicPayloadTree(0)
                CyclicPayloadTree(1)
                CyclicPayloadTree([2, 3])
                CyclicPayloadTree(2)
                CyclicPayloadTree(3)
                CyclicPayloadTree([4, 5])
                CyclicPayloadTree(4)
                CyclicPayloadTree(5)
                CyclicPayloadTree([6, 7])
                CyclicPayloadTree(6)
                CyclicPayloadTree(7)
                CyclicPayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])
                CyclicPayloadTree([0, 1])
                CyclicPayloadTree(0)
                CyclicPayloadTree(1)
                CyclicPayloadTree([2, 3])
                CyclicPayloadTree(2)
                CyclicPayloadTree(3)

        ..  container:: example

            **Example 2.** Iterates from right to left:

            ::

                >>> generator = cyclic_tree.iterate_forever_depth_first(
                ...     reverse=True)
                >>> for i in range(20):
                ...     generator.next()
                CyclicPayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])
                CyclicPayloadTree([6, 7])
                CyclicPayloadTree(7)
                CyclicPayloadTree(6)
                CyclicPayloadTree([4, 5])
                CyclicPayloadTree(5)
                CyclicPayloadTree(4)
                CyclicPayloadTree([2, 3])
                CyclicPayloadTree(3)
                CyclicPayloadTree(2)
                CyclicPayloadTree([0, 1])
                CyclicPayloadTree(1)
                CyclicPayloadTree(0)
                CyclicPayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])
                CyclicPayloadTree([6, 7])
                CyclicPayloadTree(7)
                CyclicPayloadTree(6)
                CyclicPayloadTree([4, 5])
                CyclicPayloadTree(5)
                CyclicPayloadTree(4)

        Yields cyclic payload tree nodes.
        '''
        while True:
            for node in PayloadTree.iterate_depth_first(self, reverse=reverse):
                yield node
