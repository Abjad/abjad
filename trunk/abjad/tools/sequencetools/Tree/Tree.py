from abjad.core._StrictComparator import _StrictComparator
import copy


class Tree(_StrictComparator):
    r'''.. versionadded:: 2.4

    Abjad data structure to work with a sequence whose elements have been
    grouped into arbitrarily many levels of containment.

    Example: a list of pitches that have been grouped 
    into cells that have, in turn, been grouped into groups of cells
    that have, in turn, been grouped into groups of groups of cells.
    
    ::

        abjad> from abjad.tools import sequencetools

    Here is a tree::

        abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
        abjad> tree = sequencetools.Tree(sequence)

    ::

        abjad> tree
        Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

    ::

        abjad> tree.parent is None
        True

    ::

        abjad> tree.children
        (Tree([0, 1]), Tree([2, 3]), Tree([4, 5]), Tree([6, 7]))

    ::

        abjad> tree.depth
        3

    Here's an internal node::

        abjad> tree[2]
        Tree([4, 5])

    ::

        abjad> tree[2].parent
        Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

    ::

        abjad> tree[2].children
        (Tree(4), Tree(5))

    ::

        abjad> tree[2].depth
        2

    ::

        abjad> tree[2].level
        1

    Here's a leaf node::


        abjad> tree[2][0]
        Tree(4)

    ::

        abjad> tree[2][0].parent
        Tree([4, 5])

    ::

        abjad> tree[2][0].children
        ()

    ::

        abjad> tree[2][0].depth
        1

    ::

        abjad> tree[2][0].level
        2

    ::

        abjad> tree[2][0].position
        (2, 0)

    ::

        abjad> tree[2][0].payload
        4

    Only leaf nodes carry payload. Internal nodes carry no payload.

    Negative levels are available to work with trees bottom-up instead of top-down.

    Trees do not yet implement append or extend methods.
    '''

    def __init__(self, expr):
        self._children = self._initialize_children_list()
        self.parent = None
        try:
            self.payload = None
            for element in expr:
                child = type(self)(element)
                self._children.append(child)
                child.parent = self
        except TypeError:
            self.payload = expr

    ### OVERLOADS ###

    def __contains__(self, expr):
        return expr in self._children

    def __eq__(self, other):
        if isinstance(other, type(self)):
            if self.payload is not None or other.payload is not None:
                return self.payload == other.payload
            if len(self) == len(other):
                for x, y in zip(self._noncyclic_children, other._noncyclic_children):
                    if not x == y:
                        return False
                else:
                    return True
        return False

    def __getitem__(self, expr):
        return self._children[expr]

    ## TODO: figure out why this breaks Tree.remove_to_root()
#    def __getslice__(self, start_index, stop_index):
#        result = []
#        result = [self[n] for n in range(start_index, stop_index)]
#        return result

    def __len__(self):
        return len(self._children)

    def __ne__(self, other):
        return not self == other

    def __repr__(self):
        return '%s(%s)' % (type(self).__name__, self)

    def __str__(self):
        if self.payload is None:
            return '[%s]' % ', '.join([str(x) for x in self._noncyclic_children])
        else:
            return repr(self.payload)

    ### PRIVATE ATTRIBUTES ###

    @property
    def _noncyclic_children(self):
        return list(self._children)

    ### PRIVATE METHODS ###

    def _initialize_and_wrap_nodes_with_type(self, expr, type_):
        self._children = self._initialize_children_list()
        self.parent = None
        try:
            self.payload = None
            for element in expr:
                #child = type(self)(element)
                child = type_(element)
                self._children.append(child)
                child.parent = self
        except TypeError:
            self.payload = expr

    ### PUBLIC ATTRIBUTES ###

    @property
    def children(self):
        '''.. versionadded:: 2.4

        Children of node::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].children
            (Tree(2), Tree(3))

        Return tuple of zero or more nodes.
        '''
        return tuple(self._children)

    @property
    def depth(self):
        '''.. versionadded:: 2.4

        Depth of subtree::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].depth
            2

        Return nonnegative integer.
        '''
        levels = set([])
        for node in self.iterate_depth_first():
            levels.add(node.level)
        return max(levels) - self.level + 1

    @property
    def level(self):
        '''.. versionadded:: 2.4

        Level of node::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].level
            1

        Return nonnegative integer.
        '''
        return len(self.proper_parentage)

    @property
    def improper_parentage(self):
        '''.. versionadded:: 2.4

        Improper parentage of node::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].improper_parentage
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
        '''.. versionadded:: 2.4

        Index of node in parent::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].index_in_parent
            1

        Return nonnegative integer.
        '''
        if self.parent is not None:
            return self.parent._children.index(self)
        else:
            return None

    @property
    def negative_level(self):
        '''.. versionadded:: 2.4

        Negative level of node::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].negative_level
            -2

        Return negative integer.
        '''
        return self.level - self.root.depth
        
    @property
    def position(self):
        '''.. versionadded:: 2.4

        Position of node relative to root::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].position
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
        '''.. versionadded:: 2.4

        Proper parentage of node::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].proper_parentage
            (Tree([[0, 1], [2, 3], [4, 5], [6, 7]]),)


        Return tuple of zero or more nodes.
        '''
        return self.improper_parentage[1:]
    
    @property
    def root(self):
        '''.. versionadded:: 2.4

        Root of tree::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].proper_parentage
            (Tree([[0, 1], [2, 3], [4, 5], [6, 7]]),)

        Return node.
        '''
        return self.improper_parentage[-1]

    @property
    def width(self):
        '''.. versionadded:: 2.4
    
        Number of leaves in subtree::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1].width
            2

        Return nonnegative integer.
        '''
        return len(list(self.iterate_at_level(-1))) 

    ### PRIVATE METHODS ###

    def _get_next_n_nodes_at_level_helper(self, n, level, nodes_must_be_complete = False):
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
        r'''.. versionadded:: 2.5

        Get next `n` complete nodes at `level` from node.

        ::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        With nonnegative `level`:

        Get next 4 nodes at level 2::

            abjad> tree[0][0].get_next_n_complete_nodes_at_level(4, 2)
            [Tree(1), Tree(2), Tree(3), Tree(4)]

        Get next 3 nodes at level 1::

            abjad> tree[0][0].get_next_n_complete_nodes_at_level(3, 1)
            [Tree([1]), Tree([2, 3]), Tree([4, 5]), Tree([6, 7])]

        With negative `level`:
        
        Get next 4 nodes at level -1::

            abjad> tree[0][0].get_next_n_complete_nodes_at_level(4, -1)
            [Tree(1), Tree(2), Tree(3), Tree(4)]

        Get next 3 nodes at level -2::

            abjad> tree[0][0].get_next_n_complete_nodes_at_level(3, -2)
            [Tree([1]), Tree([2, 3]), Tree([4, 5]), Tree([6, 7])]

        Trim first node if necessary.

        Return list of nodes.
        '''
        return self._get_next_n_nodes_at_level_helper(n, level, nodes_must_be_complete = True)
        
    def get_next_n_nodes_at_level(self, n, level):
        r'''.. versionadded:: 2.4

        Get next `n` nodes at `level` from node.

        ::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        With nonnegative `level`:

        Get next 4 nodes at level 2::

            abjad> tree[0][0].get_next_n_nodes_at_level(4, 2)
            [Tree(1), Tree(2), Tree(3), Tree(4)]

        Get next 3 nodes at level 1::

            abjad> tree[0][0].get_next_n_nodes_at_level(3, 1)
            [Tree([1]), Tree([2, 3]), Tree([4, 5])]

        Get next node at level 0::

            abjad> tree[0][0].get_next_n_nodes_at_level(1, 0)
            [Tree([[1], [2, 3], [4, 5], [6, 7]])]

        With negative `level`:
        
        Get next 4 nodes at level -1::

            abjad> tree[0][0].get_next_n_nodes_at_level(4, -1)
            [Tree(1), Tree(2), Tree(3), Tree(4)]

        Get next 3 nodes at level -2::

            abjad> tree[0][0].get_next_n_nodes_at_level(3, -2)
            [Tree([1]), Tree([2, 3]), Tree([4, 5])]

        Trim first node if necessary.

        Return list of nodes.
        '''
        return self._get_next_n_nodes_at_level_helper(n, level, nodes_must_be_complete = False)

    def get_node_at_position(self, position):
        '''.. versionadded:: 2.4

        Get node at `position`::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree.get_node_at_position((2, 1))
            Tree(5)

        Return node.
        '''
        result = self
        for idx in position:
            result = result[idx]
        return result

    def get_position_of_descendant(self, descendant):
        r'''.. versionadded:: 2.4

        Get position of `descendent` relative to node rather than relative to root::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[3].get_position_of_descendant(tree[3][0])
            (0,)

        Return tuple of zero or more nonnegative integers.
        ''' 
        if descendant is self:
            return ()
        else:
            return descendant.position[len(self.position):]

    def is_at_level(self, level):
        r'''.. versionadded:: 2.4

        True when node is at `level` in tree::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree[1][1].is_at_level(-1)
            True

        False otherwise::

            abjad> tree[1][1].is_at_level(0)
            False

        Return boolean.

        Predicate works for positive, negative and zero-valued `level`.
        '''
        if (0 <= level and self.level == level) or self.negative_level == level:
            return True
        else:
            return False

    def iterate_at_level(self, level):
        r'''.. versionadded:: 2.4

        Iterate depth at `level`::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> for x in tree.iterate_at_level(0): x
            ... 
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

        ::

            abjad> for x in tree.iterate_at_level(1): x
            ... 
            Tree([0, 1])
            Tree([2, 3])
            Tree([4, 5])
            Tree([6, 7])

        ::

            abjad> for x in tree.iterate_at_level(2): x
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

            abjad> for x in tree.iterate_at_level(-1): x
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

            abjad> for x in tree.iterate_at_level(-2): x
            ... 
            Tree([0, 1])
            Tree([2, 3])
            Tree([4, 5])
            Tree([6, 7])

        ::

            abjad> for x in tree.iterate_at_level(-3): x
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
        '''.. versionadded:: 2.4

        Iterate tree depth-first::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> for node in tree.iterate_depth_first(): node
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
        r'''.. versionadded:: 2.4

        Iterate tree payload::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> for element in tree.iterate_payload():
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
        r'''.. versionadded:: 2.4

        Remove `node` from tree::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree.remove(tree[1])

        ::

            abjad> tree
            Tree([[0, 1], [4, 5], [6, 7]])

        Return none.
        '''
        node.parent._children.remove(node)
        node.parent = None

    def remove_to_root(self):
        r'''.. versionadded:: 2.4

        Remove node and all nodes left of node to root::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]

        ::

            abjad> tree = sequencetools.Tree(sequence)
            abjad> tree[0][0].remove_to_root()
            abjad> tree
            Tree([[1], [2, 3], [4, 5], [6, 7]])

        ::

            abjad> tree = sequencetools.Tree(sequence)
            abjad> tree[0][1].remove_to_root()
            abjad> tree
            Tree([[2, 3], [4, 5], [6, 7]])

        ::

            abjad> tree = sequencetools.Tree(sequence)
            abjad> tree[1].remove_to_root()
            abjad> tree
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
        r'''.. versionadded:: 2.5

        Change tree to nested lists::

            abjad> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            abjad> tree = sequencetools.Tree(sequence)

        ::

            abjad> tree
            Tree([[0, 1], [2, 3], [4, 5], [6, 7]])

        ::

            abjad> tree.to_nested_lists()
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
