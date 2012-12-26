from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class TreeNode(AbjadObject):
    '''A node in a generalized tree.

    Return `TreeNode` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_parent',)

    ### INITIALIZER ###

    def __init__(self):
        self._parent = None    

    ### SPECIAL METHODS ###

    ### PRIVATE METHODS ###

    def _get_node_state_flags(self):
        state_flags = {}
        for name in self._state_flag_names:
            state_flags[name] = True
            for node in self.improper_parentage:
                if not getattr(node, name):
                    state_flags[name] = False
                    break
        return state_flags

    def _mark_entire_tree_for_later_update(self):
        for node in self.improper_parentage:
            for name in self._state_flag_names:
                setattr(node, name, False)

    def _switch_parent(self, new_parent):
        if self._parent is not None:
            index = self._parent.index(self)
            self._parent._children.pop(index)
        self._parent = new_parent
        self._mark_entire_tree_for_later_update()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _state_flag_names(self):
        return ()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def depth(self):
        '''The depth of a node in a rhythm-tree structure:

        ::

            >>> rtm = '(4 ((2 (1 1)) (2 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
        
        ::

            >>> tree.depth
            0

        ::

            >>> tree[0].depth
            1

        ::

            >>> tree[0][0].depth
            2

        Return int.
        '''
        node = self
        depth = 0
        while node.parent is not None:
            depth += 1
            node = node.parent
        return depth

    @property
    def depthwise_inventory(self):
        '''A dictionary of all nodes in a rhythm-tree, organized by their
        depth relative the root node:

        ::

            >>> rtm = '(4 ((2 (1 1)) (2 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
            >>> inventory = tree.depthwise_inventory
            >>> for depth in sorted(inventory):
            ...     print 'DEPTH: {}'.format(depth)
            ...     for node in inventory[depth]:
            ...         print str(node.duration), str(node.start_offset)
            ...
            DEPTH: 0
            4 0
            DEPTH: 1
            2 0
            2 2
            DEPTH: 2
            1 0
            1 1
            1 2
            1 3

        Return dictionary.
        '''
        inventory = {}
        def recurse(node):
            if node.depth not in inventory:
                inventory[node.depth] = []
            inventory[node.depth].append(node)
            if hasattr(node, 'children'):
                for child in node.children:
                    recurse(child)
        recurse(self)
        return inventory

    @property
    def graph_order(self):
        order = []
        for parent, child in sequencetools.iterate_sequence_pairwise_strict(
            reversed(self.improper_parentage)):
            order.append(parent.index(child))
        return tuple(order)

    @property
    def improper_parentage(self):
        '''The improper parentage of a node in a rhythm-tree, being the 
        sequence of node beginning with itself and ending with the root node
        of the tree:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeContainer()
            >>> c = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.append(b)
            >>> b.append(c)

        ::

            >>> a.improper_parentage == (a,)
            True

        ::

            >>> b.improper_parentage == (b, a)
            True

        ::

            >>> c.improper_parentage == (c, b, a)
            True

        Return tuple of `RhythmTreeNode` instances.
        '''
        node = self
        parentage = [node]
        while node.parent is not None:
            node = node.parent
            parentage.append(node)
        return tuple(parentage)

    @property
    def parent(self):
        '''The node's parent node:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeContainer()
            >>> c = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.append(b)
            >>> b.append(c)

        ::

            >>> a.parent is None
            True

        ::

            >>> b.parent is a
            True

        ::

            >>> c.parent is b
            True

        Return `RhythmTreeNode` instance.
        '''
        return self._parent

    @property
    def proper_parentage(self):
        '''The proper parentage of a node in a rhythm-tree, being the 
        sequence of node beginning with the node's immediate parent and
        ending with the root node of the tree:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeContainer()
            >>> c = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.append(b)
            >>> b.append(c)

        ::

            >>> a.proper_parentage == ()
            True

        ::

            >>> b.proper_parentage == (a,)
            True

        ::

            >>> c.proper_parentage == (b, a)
            True

        Return tuple of `RhythmTreeNode` instances.
        '''
        return self.improper_parentage[1:]

    @property
    def root(self):
        '''The root node of the tree: that node in the tree which has
        no parent:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeContainer()
            >>> c = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.append(b)
            >>> b.append(c)

        ::

            >>> a.root is a
            True
            >>> b.root is a
            True
            >>> c.root is a
            True

        Return `TreeNode` instance.
        '''
        node = self
        while node.parent is not None:
            node = node.parent
        return node

