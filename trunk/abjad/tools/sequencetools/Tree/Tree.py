import copy
from abjad.tools.abctools.AbjadObject import AbjadObject


class Tree(AbjadObject):
    r'''.. versionadded:: 2.4

    Abjad data structure to work with a sequence whose elements have been
    grouped into arbitrarily many levels of containment.

    Here is a tree:

    ::

        >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
        >>> tree = sequencetools.Tree(sequence)

    ::

        >>> tree
        Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

    ::

        >>> tree.parent is None
        True

    ::

        >>> tree.children
        (Tree([0, 1]), Tree([2, 3]), Tree([4, 5]), Tree([6, 7]))

    ::

        >>> tree.depth
        3

    Here's an internal node:

    ::

        >>> tree[2]
        Tree([4, 5])

    ::

        >>> tree[2].parent
        Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

    ::

        >>> tree[2].children
        (Tree(4), Tree(5))

    ::

        >>> tree[2].depth
        2

    ::

        >>> tree[2].level
        1

    Here's a leaf node:

    ::

        >>> tree[2][0]
        Tree(4)

    ::

        >>> tree[2][0].parent
        Tree([4, 5])

    ::

        >>> tree[2][0].children
        ()

    ::

        >>> tree[2][0].depth
        1

    ::

        >>> tree[2][0].level
        2

    ::

        >>> tree[2][0].position
        (2, 0)

    ::

        >>> tree[2][0].payload
        4

    Only leaf nodes carry payload. Internal nodes carry no payload.

    Negative levels are available to work with trees bottom-up instead of top-down.

    Trees do not yet implement append or extend methods.
    '''

    ### INITIALIZER ###

    def __init__(self, expr):
        self._children = self._initialize_children_list()
        self.parent = None
        try:
            self._payload = None
            for element in expr:
                child = type(self)(element)
                self._children.append(child)
                child.parent = self
        except TypeError:
            self._payload = expr

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        '''True when tree contains `expr`:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[-1] in tree
            True

        Otherwise false:

            >>> tree[-1][-1] in tree
            False

        Return boolean.
        '''
        return expr in self._children

    def __eq__(self, expr):
        '''True when `expr` is the same type as tree
        and when the payload of all subtrees are equal:

        ::

            >>> sequence_1 = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree_1 = sequencetools.Tree(sequence_1)
            >>> sequence_2 = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree_2 = sequencetools.Tree(sequence_2)
            >>> sequence_3 = [[0, 1], [2, 3], [4, 5]]
            >>> tree_3 = sequencetools.Tree(sequence_3)

        ::

            >>> tree_1 == tree_1
            True
            >>> tree_1 == tree_2
            True
            >>> tree_1 == tree_3
            False
            >>> tree_2 == tree_1
            True
            >>> tree_2 == tree_2
            True
            >>> tree_2 == tree_3
            False
            >>> tree_3 == tree_1
            False
            >>> tree_3 == tree_2
            False
            >>> tree_3 == tree_3
            True

        Return boolean.
        '''
        if isinstance(expr, type(self)):
            if self.payload is not None or expr.payload is not None:
                return self.payload == expr.payload
            if len(self) == len(expr):
                for x, y in zip(self._noncyclic_children, expr._noncyclic_children):
                    if not x == y:
                        return False
                else:
                    return True
        return False

    def __getitem__(self, expr):
        '''Get item from tree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[-1]
            Tree([6, 7])

        Get slice from tree:

        ::

            >>> tree[-2:]
            [Tree([4, 5]), Tree([6, 7])]

        Return node.
        '''
        return self._children[expr]

    def __len__(self):
        '''Return the number of children in tree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> len(tree)
            4
    
        Return nonnegative integer.
        '''
        return len(self._children)

    def __repr__(self):
        '''Interpreter representation of tree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])
        
        Return string.
        '''
        return '%s(%s)' % (type(self).__name__, self)

    def __str__(self):
        '''String representation of tree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> str(tree)
            '[[0, 1], [2, 3], [4, 5], [6, 7]]'

        Return string.
        '''
        if self.payload is None:
            return '[%s]' % ', '.join([str(x) for x in self._noncyclic_children])
        else:
            return repr(self.payload)

    ### PRIVATE PROPERTIES ###

    @property
    def _input_argument(self):
        return eval(str(self))

    @property
    def _noncyclic_children(self):
        return list(self._children)

    @property
    def _positional_argument_values(self):
        return self._input_argument

    @property
    def _tools_package_qualified_repr(self):
        for part in reversed(type(self).__module__.split('.')):
            if not part == type(self).__name__:
                tools_package = part
                break
        return '{}.{}({})'.format(tools_package, type(self).__name__, self)

    ### PRIVATE METHODS ###

    def _initialize_and_wrap_nodes_with_type(self, expr, type_):
        self._children = self._initialize_children_list()
        self.parent = None
        try:
            self.payload = None
            for element in expr:
                child = type_(element)
                self._children.append(child)
                child.parent = self
        except TypeError:
            self.payload = expr

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        '''Children of node:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].children
            (Tree(2), Tree(3))

        Return tuple of zero or more nodes.
        '''
        return tuple(self._children)

    @property
    def depth(self):
        '''Depth of subtree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].depth
            2

        Return nonnegative integer.
        '''
        levels = set([])
        for node in self.iterate_depth_first():
            levels.add(node.level)
        return max(levels) - self.level + 1

    @property
    def improper_parentage(self):
        '''Improper parentage of node:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].improper_parentage
            (Tree([2, 3]), Tree([[0, 1], [2, 3], [4, 5], [6, 7]]))

        Return tuple of one or more nodes.
        '''
        result = [self]
        cur = self.parent
        while cur is not None:
            result.append(cur)
            cur = cur.parent
        return tuple(result)

    @property
    def index_in_parent(self):
        '''Index of node in parent of node:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].index_in_parent
            1

        Return nonnegative integer.
        '''
        if self.parent is not None:
            #return self.parent._children.index(self)
            return self.parent.index(self)
        else:
            return None

    @property
    def level(self):
        '''Level of node:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].level
            1

        Return nonnegative integer.
        '''
        return len(self.proper_parentage)

    @property
    def manifest_payload(self):
        '''Manifest payload of tree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)
    
        ::

            >>> tree.manifest_payload
            [0, 1, 2, 3, 4, 5, 6, 7]

        ::

            >>> tree[-1].manifest_payload
            [6, 7]

        ::

            >>> tree[-1][-1].manifest_payload
            [7]

        Return list.
        '''
        if 0 <= self.level:
            return [x.payload for x in self.iterate_at_level(-1)]
        else:
            return [self.payload]

    @property
    def negative_level(self):
        '''Negative level of node:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].negative_level
            -2

        Return negative integer.
        '''
        return self.level - self.root.depth
        
    @property
    def payload(self):
        '''Payload of node:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)
    
        Return none for interior node:

        ::

            >>> tree.payload is None
            True

        ::

            >>> tree[-1].payload is None
            True

        Return unwrapped payload for leaf node:

            >>> tree[-1][-1].payload
            7

        Return arbitrary expression or none.
        '''
        return self._payload
        
    @property
    def position(self):
        '''Position of node relative to root:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].position
            (1,)

        Return tuple of zero or more nonnegative integers.
        '''
        result = []
        for node in self.improper_parentage:
            if node.parent is not None:
                result.append(node.index_in_parent)
        result.reverse()
        return tuple(result)

    @property
    def proper_parentage(self):
        '''Proper parentage of node:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].proper_parentage
            (Tree([[0, 1], [2, 3], [4, 5], [6, 7]]),)


        Return tuple of zero or more nodes.
        '''
        return self.improper_parentage[1:]
    
    @property
    def root(self):
        '''Root of tree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].proper_parentage
            (Tree([[0, 1], [2, 3], [4, 5], [6, 7]]),)

        Return node.
        '''
        return self.improper_parentage[-1]

    @property
    def storage_format(self):
        '''Tree storage format:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::
    
            >>> z(tree)
            sequencetools.Tree(
                [0, 1],
                [2, 3],
                [4, 5],
                [6, 7]
                )

        Return string.
        '''
        return AbjadObject.storage_format.fget(self)
    
    @property
    def width(self):
        '''Number of leaves in subtree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1].width
            2

        Return nonnegative integer.
        '''
        return len(list(self.iterate_at_level(-1))) 

    ### PRIVATE METHODS ###

    def _get_next_n_nodes_at_level_helper(self, n, level, nodes_must_be_complete=False):
        result = []
        self_is_found = False
        first_node_returned_is_trimmed = False
        for node in self.root.iterate_depth_first():
            if len(result) == n:
                if not first_node_returned_is_trimmed or \
                    not nodes_must_be_complete:
                    return result
            if len(result) == n + 1:
                return result
            if node is self:
                self_is_found = True
                # test whether node to return is higher in tree than self;
                # or-clause allows for test of either nonnegative or negative level
                if ((0 <= level) and level < self.level) or \
                   ((level < 0) and level < self.negative_level):
                    first_node_returned_is_trimmed = True
                    subtree_to_trim = node.parent
                    # find subtree to trim where level is nonnegative
                    if 0 <= level:
                        while level < subtree_to_trim.level:
                            subtree_to_trim = subtree_to_trim.parent
                    # find subtree to trim where level is negative
                    else:
                        while subtree_to_trim.negative_level < level:
                            subtree_to_trim = subtree_to_trim.parent
                    position_of_descendant = subtree_to_trim.get_position_of_descendant(node)
                    first_subtree = copy.deepcopy(subtree_to_trim)
                    reference_node = first_subtree.get_node_at_position(position_of_descendant)
                    reference_node.remove_to_root()
                    result.append(first_subtree)
            if self_is_found:
                if node is not self:
                    if node.is_at_level(level):
                        result.append(node)
        else:
            raise ValueError('not enough nodes remain at level %s.' % level)

    def _initialize_children_list(self):
        return []

    ### PUBLIC METHODS ###

    def get_next_n_complete_nodes_at_level(self, n, level):
        r'''Get next `n` complete nodes at `level` from node.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        Get next 4 nodes at level 2:

        ::

            >>> tree[0][0].get_next_n_complete_nodes_at_level(4, 2)
            [Tree(1), Tree(2), Tree(3), Tree(4)]

        Get next 3 nodes at level 1:

        ::

            >>> tree[0][0].get_next_n_complete_nodes_at_level(3, 1)
            [Tree([1]), Tree([2, 3]), Tree([4, 5]), Tree([6, 7])]

        Get next 4 nodes at level -1:

        ::

            >>> tree[0][0].get_next_n_complete_nodes_at_level(4, -1)
            [Tree(1), Tree(2), Tree(3), Tree(4)]

        Get next 3 nodes at level -2:

        ::

            >>> tree[0][0].get_next_n_complete_nodes_at_level(3, -2)
            [Tree([1]), Tree([2, 3]), Tree([4, 5]), Tree([6, 7])]

        Trim first node if necessary.

        Return list of nodes.
        '''
        return self._get_next_n_nodes_at_level_helper(n, level, nodes_must_be_complete=True)
        
    def get_next_n_nodes_at_level(self, n, level):
        r'''Get next `n` nodes at `level` from node.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        Get next 4 nodes at level 2:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(4, 2)
            [Tree(1), Tree(2), Tree(3), Tree(4)]

        Get next 3 nodes at level 1:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(3, 1)
            [Tree([1]), Tree([2, 3]), Tree([4, 5])]

        Get next node at level 0:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(1, 0)
            [Tree([[1], [2, 3], [4, 5], [6, 7]])]

        Get next 4 nodes at level -1:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(4, -1)
            [Tree(1), Tree(2), Tree(3), Tree(4)]

        Get next 3 nodes at level -2:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(3, -2)
            [Tree([1]), Tree([2, 3]), Tree([4, 5])]

        Trim first node if necessary.

        Return list of nodes.
        '''
        return self._get_next_n_nodes_at_level_helper(n, level, nodes_must_be_complete=False)

    def get_node_at_position(self, position):
        '''Get node at `position`:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree.get_node_at_position((2, 1))
            Tree(5)

        Return node.
        '''
        result = self
        for idx in position:
            result = result[idx]
        return result

    def get_position_of_descendant(self, descendant):
        r'''Get position of `descendent` relative to node rather than relative to root:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[3].get_position_of_descendant(tree[3][0])
            (0,)

        Return tuple of zero or more nonnegative integers.
        ''' 
        if descendant is self:
            return ()
        else:
            return descendant.position[len(self.position):]

    def index(self, node):
        '''Index of `node`:

        ::

            >>> sequence = [0, 1, 2, 2, 3, 4]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> for node in tree:
            ...     node, tree.index(node)
            (Tree(0), 0)
            (Tree(1), 1)
            (Tree(2), 2)
            (Tree(2), 3)
            (Tree(3), 4)
            (Tree(4), 5)

        Return nonnegative integer.
        '''
        for i, current_node in enumerate(self):
            if current_node is node:
                return i
        raise ValueError('{!r} is not in tree.'.format(node))

    def is_at_level(self, level):
        r'''True when node is at `level` in containing tree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree[1][1].is_at_level(-1)
            True

        False otherwise::

            >>> tree[1][1].is_at_level(0)
            False

        Works for positive, negative and zero-valued `level`.

        Return boolean.
        '''
        if (0 <= level and self.level == level) or self.negative_level == level:
            return True
        else:
            return False

    def iterate_at_level(self, level):
        r'''Iterate tree at `level`:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> for x in tree.iterate_at_level(0): x
            ... 
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

        ::

            >>> for x in tree.iterate_at_level(1): x
            ... 
            Tree([0, 1])
            Tree([2, 3])
            Tree([4, 5])
            Tree([6, 7])

        ::

            >>> for x in tree.iterate_at_level(2): x
            ... 
            Tree(0)
            Tree(1)
            Tree(2)
            Tree(3)
            Tree(4)
            Tree(5)
            Tree(6)
            Tree(7)

        ::

            >>> for x in tree.iterate_at_level(-1): x
            ... 
            Tree(0)
            Tree(1)
            Tree(2)
            Tree(3)
            Tree(4)
            Tree(5)
            Tree(6)
            Tree(7)

        ::

            >>> for x in tree.iterate_at_level(-2): x
            ... 
            Tree([0, 1])
            Tree([2, 3])
            Tree([4, 5])
            Tree([6, 7])

        ::

            >>> for x in tree.iterate_at_level(-3): x
            ... 
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

        Return node generator.
        '''
        for x in self.iterate_depth_first():
            if 0 <= level:
                if x.level == level:
                    yield x
            else:
                if x.negative_level == level:
                    yield x

    def iterate_depth_first(self):
        '''Iterate tree depth-first:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> for node in tree.iterate_depth_first(): node
            ... 
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])
            Tree([0, 1])
            Tree(0)
            Tree(1)
            Tree([2, 3])
            Tree(2)
            Tree(3)
            Tree([4, 5])
            Tree(4)
            Tree(5)
            Tree([6, 7])
            Tree(6)
            Tree(7)

        Return node generator.
        '''
        yield self
        for x in self:
            for y in x.iterate_depth_first():
                yield y

    def iterate_payload(self):
        r'''Iterate tree payload:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> for element in tree.iterate_payload():
            ...     element
            ... 
            0
            1
            2
            3
            4
            5
            6
            7

        Return payload generator.
        '''
        for leaf_node in self.iterate_at_level(-1):
            yield leaf_node.payload

    def remove(self, node):
        r'''Remove `node` from tree:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree.remove(tree[1])

        ::

            >>> tree
            Tree([[0, 1], [4, 5], [6, 7]])

        Return none.
        '''
        node.parent._children.remove(node)
        node.parent = None

    def remove_to_root(self):
        r'''Remove node and all nodes left of node to root:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]

        ::

            >>> tree = sequencetools.Tree(sequence)
            >>> tree[0][0].remove_to_root()
            >>> tree
            Tree([[1], [2, 3], [4, 5], [6, 7]])

        ::

            >>> tree = sequencetools.Tree(sequence)
            >>> tree[0][1].remove_to_root()
            >>> tree
            Tree([[2, 3], [4, 5], [6, 7]])

        ::

            >>> tree = sequencetools.Tree(sequence)
            >>> tree[1].remove_to_root()
            >>> tree
            Tree([[4, 5], [6, 7]])

        Modify in-place to root.

        Return none.
        '''
        ## trim left-siblings of self and self
        parent = self.parent
        for sibling in parent[:]:
            sibling.parent.remove(sibling)
            ## break and do not remove siblings to right of self
            if sibling is self:
                break
        ## trim parentage
        for node in parent.improper_parentage:
            if node.parent is not None:
                for sibling in node.parent[:]:
                    if sibling is node:
                        # remove node now if it was emptied earlier
                        if not len(sibling):
                            sibling.parent.remove(sibling)
                        break
                    else:
                        sibling.parent.remove(sibling) 
    
    def to_nested_lists(self):
        r'''Change tree to nested lists:

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = sequencetools.Tree(sequence)

        ::

            >>> tree
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

        ::

            >>> tree.to_nested_lists()
            [[0, 1], [2, 3], [4, 5], [6, 7]]

        Return list of lists.
        '''
        if self.payload is not None:
            raise TypeError('leaf node is not iterable.')
        else:
            result = []
            for child in self._noncyclic_children:
                if child.payload is not None:
                    result.append(child.payload)
                else:
                    result.append(child.to_nested_lists())
            return result
