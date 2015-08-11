# -*- encoding: utf-8 -*-
import copy
from abjad.tools.abctools.AbjadObject import AbjadObject


class PayloadTree(AbjadObject):
    r'''A payload tree.

    Abjad data structure to work with a sequence whose elements have been
    grouped into arbitrarily many levels of containment.

    Here is a tree:

    ::

        >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
        >>> tree = datastructuretools.PayloadTree(sequence)

    ::

        >>> tree
        PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])

    ::

        >>> tree.parent is None
        True

    ::

        >>> for x in tree.children:
        ...     x
        PayloadTree([0, 1])
        PayloadTree([2, 3])
        PayloadTree([4, 5])
        PayloadTree([6, 7])

    ::

        >>> tree.depth
        3

    Here's an internal node:

    ::

        >>> tree[2]
        PayloadTree([4, 5])

    ::

        >>> tree[2].parent
        PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])

    ::

        >>> tree[2].children
        (PayloadTree(4), PayloadTree(5))

    ::

        >>> tree[2].depth
        2

    ::

        >>> tree[2].level
        1

    Here's a leaf node:

    ::

        >>> tree[2][0]
        PayloadTree(4)

    ::

        >>> tree[2][0].parent
        PayloadTree([4, 5])

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

    Negative levels are available to work with trees bottom-up
    instead of top-down.

    Trees do not yet implement append or extend methods.
    '''

    ### INITIALIZER ###

    def __init__(self, expr=None, item_class=None):
        if isinstance(expr, type(self)):
            expr = expr.to_nested_lists()
        self._children = self._initialize_children_list()
        self.parent = None
        self._item_class = item_class
        if isinstance(expr, str):
            self._payload = expr
        else:
            self._payload = None
            try:
                for element in expr:
                    child = type(self)(element, item_class=self.item_class)
                    self._children.append(child)
                    child.parent = self
            except TypeError:
                self._payload = expr
        if self.item_class is not None:
            for node in self.iterate_at_level(-1):
                pitch_class = self.item_class(node.payload)
                node._payload = pitch_class

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        r'''Is true when payload tree contains `expr`.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[-1] in tree
            True

        Otherwise false:

            >>> tree[-1][-1] in tree
            False

        Returns boolean.
        '''
        return expr in self._children

    def __eq__(self, expr):
        r'''Is true when `expr` is the same type as tree
        and when the payload of all subtrees are equal.

        ::

            >>> sequence_1 = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree_1 = datastructuretools.PayloadTree(sequence_1)
            >>> sequence_2 = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree_2 = datastructuretools.PayloadTree(sequence_2)
            >>> sequence_3 = [[0, 1], [2, 3], [4, 5]]
            >>> tree_3 = datastructuretools.PayloadTree(sequence_3)

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

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.payload is not None or expr.payload is not None:
                return self.payload == expr.payload
            if len(self) == len(expr):
                for x, y in zip(
                    self._noncyclic_children, expr._noncyclic_children):
                    if not x == y:
                        return False
                else:
                    return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats payload tree.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> print(format(tree))
            datastructuretools.PayloadTree(
                [
                    [0, 1],
                    [2, 3],
                    [4, 5],
                    [6, 7],
                    ]
                )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __getitem__(self, expr):
        r'''Gets `expr` from payload tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[-1]
            PayloadTree([6, 7])

        Gets slice from payload tree:

        ::

            >>> tree[-2:]
            (PayloadTree([4, 5]), PayloadTree([6, 7]))

        Returns node.
        '''
        return self.children[expr]

    def __getstate__(self):
        r'''Gets object state.
        '''
        return vars(self)

    def __graph__(self, **kwargs):
        r'''The GraphvizGraph representation of payload tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree_graph = tree.__graph__()
            >>> print(str(tree_graph))
            digraph G {
                graph [bgcolor=transparent,
                    truecolor=true];
                node_0 [label="",
                    shape=circle];
                node_1 [label="",
                    shape=circle];
                node_2 [label=0,
                    shape=box];
                node_3 [label=1,
                    shape=box];
                node_4 [label="",
                    shape=circle];
                node_5 [label=2,
                    shape=box];
                node_6 [label=3,
                    shape=box];
                node_7 [label="",
                    shape=circle];
                node_8 [label=4,
                    shape=box];
                node_9 [label=5,
                    shape=box];
                node_10 [label="",
                    shape=circle];
                node_11 [label=6,
                    shape=box];
                node_12 [label=7,
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_4;
                node_0 -> node_7;
                node_0 -> node_10;
                node_1 -> node_2;
                node_1 -> node_3;
                node_4 -> node_5;
                node_4 -> node_6;
                node_7 -> node_8;
                node_7 -> node_9;
                node_10 -> node_11;
                node_10 -> node_12;
            }

        ::

            >>> graph(tree) # doctest: +SKIP

        Returns graphviz graph.
        '''
        from abjad.tools import documentationtools
        graph = documentationtools.GraphvizGraph(
            attributes={
                'bgcolor': 'transparent',
                'truecolor': True,
                },
            name='G',
            )
        node_mapping = {}
        for node in self.iterate_depth_first():
            graphviz_node = documentationtools.GraphvizNode()
            if node.children:
                graphviz_node.attributes['shape'] = 'circle'
                graphviz_node.attributes['label'] = '""'
            else:
                graphviz_node.attributes['shape'] = 'box'
                graphviz_node.attributes['label'] = str(node.payload)
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node.parent is not None:
                documentationtools.GraphvizEdge().attach(
                    node_mapping[node.parent],
                    node_mapping[node],
                    )
        return graph

    def __hash__(self):
        r'''Hashes payload tree.

        Required to be explicitly re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(PayloadTree, self).__hash__()

    def __len__(self):
        r'''Number of children in payload tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> len(tree)
            4

        Returns nonnegative integer.
        '''
        return len(self._children)

    def __repr__(self):
        r'''Gets interpreter representation of payload tree.

        ..  container:: example

            Typical payload tree:

            ::

                >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> datastructuretools.PayloadTree(sequence)
                PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])

        ..  container:: example

            Payload tree leaf:

            ::

                >>> datastructuretools.PayloadTree(0)
                PayloadTree(0)

        ..  container:: example

            Empty payload tree:

            ::

                >>> datastructuretools.PayloadTree()
                PayloadTree([])

        Returns string.
        '''
        return AbjadObject.__repr__(self)

    ### PRIVATE PROPERTIES ###

    @property
    def _noncyclic_children(self):
        return list(self._children)

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = []
        if self.payload is not None:
            positional_argument_values.append(self.payload)
        elif self.depth == 0:
            pass
        else:
            nested_lists = self.to_nested_lists()
            positional_argument_values.append(nested_lists)
        positional_argument_values = tuple(positional_argument_values)
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )

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
        r'''Children of payload tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].children
            (PayloadTree(2), PayloadTree(3))

        Returns tuple of zero or more nodes.
        '''
        return tuple(self._children)

    @property
    def depth(self):
        r'''Depth of payload tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].depth
            2

        Returns nonnegative integer.
        '''
        levels = set([])
        for node in self.iterate_depth_first():
            levels.add(node.level)
        return max(levels) - self.level + 1

    @property
    def expr(self):
        r'''Gets input argument.
        '''
        return self._expr

    @property
    def improper_parentage(self):
        r'''Improper parentage of payload tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].improper_parentage
            (PayloadTree([2, 3]), PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]]))

        Returns tuple of one or more nodes.
        '''
        result = [self]
        current = self.parent
        while current is not None:
            result.append(current)
            current = current.parent
        return tuple(result)

    @property
    def index_in_parent(self):
        r'''Index of node in parent of node.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].index_in_parent
            1

        Returns nonnegative integer.
        '''
        if self.parent is not None:
            return self.parent.index(self)
        else:
            return None

    @property
    def item_class(self):
        r'''Gets item class of payload tree.

        ..  container:: example

            ::

                >>> tree.item_class is None
                True

        ..  container:: example

            Set item class to coerce input at initialization::

                >>> tree = datastructuretools.PayloadTree(
                ...     expr=[[1.1, 2.2], [8.8, 9.9]],
                ...     item_class=int,
                ...     )
                >>> tree
                PayloadTree([[1, 2], [8, 9]])

        Returns class or none.
        '''
        return self._item_class

    @property
    def level(self):
        r'''Level of node.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].level
            1

        Returns nonnegative integer.
        '''
        return len(self.proper_parentage)

    @property
    def manifest_payload(self):
        r'''Manifest payload of payload tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree.manifest_payload
            [0, 1, 2, 3, 4, 5, 6, 7]

        ::

            >>> tree[-1].manifest_payload
            [6, 7]

        ::

            >>> tree[-1][-1].manifest_payload
            [7]

        Returns list.
        '''
        if 0 <= self.level:
            return [x.payload for x in self.iterate_at_level(-1)]
        else:
            return [self.payload]

    @property
    def negative_level(self):
        r'''Negative level of node.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].negative_level
            -2

        Returns negative integer.
        '''
        return self.level - self.root.depth

    @property
    def payload(self):
        r'''Payload of node.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        Returns none for interior node:

        ::

            >>> tree.payload is None
            True

        ::

            >>> tree[-1].payload is None
            True

        Returns unwrapped payload for leaf node:

            >>> tree[-1][-1].payload
            7

        Returns arbitrary expression or none.
        '''
        return self._payload

    @property
    def position(self):
        r'''Position of node relative to root.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].position
            (1,)

        Returns tuple of zero or more nonnegative integers.
        '''
        result = []
        for node in self.improper_parentage:
            if node.parent is not None:
                result.append(node.index_in_parent)
        result.reverse()
        return tuple(result)

    @property
    def proper_parentage(self):
        r'''Proper parentage of node.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].proper_parentage
            (PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]]),)


        Returns tuple of zero or more nodes.
        '''
        return self.improper_parentage[1:]

    @property
    def root(self):
        r'''Root of payload tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].proper_parentage
            (PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]]),)

        Returns node.
        '''
        return self.improper_parentage[-1]

    @property
    def width(self):
        r'''Number of leaves in payload tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1].width
            2

        Returns nonnegative integer.
        '''
        return len(list(self.iterate_at_level(-1)))

    ### PRIVATE METHODS ###

    def _get_next_n_nodes_at_level_helper(
        self,
        n,
        level,
        nodes_must_be_complete=False,
        ):
        if not self._is_valid_level(level):
            message = 'invalid level: {!r}.'.format(level)
            raise Exception(message)
        result = []
        self_is_found = False
        first_node_returned_is_trimmed = False
        if n < 0:
            reverse = True
        else:
            reverse = False
        n = abs(n)
        if hasattr(self.root, 'iterate_forever_depth_first'):
            generator = self.root.iterate_forever_depth_first(reverse=reverse)
        else:
            generator = self.root.iterate_depth_first(reverse=reverse)
        previous_node = None
        for node in generator:
            if len(result) == n:
                if not first_node_returned_is_trimmed or \
                    not nodes_must_be_complete:
                    return result
            if len(result) == n + 1:
                return result
            if node is self:
                self_is_found = True
                # test whether node to return is higher in tree than self;
                # or-clause allows for test of either nonnegative
                # or negative level
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
                    position_of_descendant = \
                        subtree_to_trim.get_position_of_descendant(node)
                    first_subtree = copy.deepcopy(subtree_to_trim)
                    reference_node = \
                        first_subtree.get_node_at_position(
                            position_of_descendant)
                    reference_node.remove_to_root(reverse=reverse)
                    result.append(first_subtree)
            if self_is_found:
                if node is not self:
                    if node.is_at_level(level):
                        result.append(node)
                    # special case to handle a cyclic tree of length 1
                    elif node.is_at_level(0) and len(node) == 1:
                        if previous_node.is_at_level(level):
                            result.append(node)
            previous_node = node
        else:
            message = 'not enough nodes at level {}.'
            message = message.format(level)
            raise ValueError(message)

    def _initialize_children_list(self):
        return []

    def _is_valid_level(self, level):
        maximum_absolute_level = self.depth + 1
        if maximum_absolute_level < abs(level):
            return False
        return True

    ### PUBLIC METHODS ###

    def get_manifest_payload_of_next_n_nodes_at_level(self, n, level):
        r'''Gets manifest payload of next `n` nodes at `level` from node.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        Gets manifest paylaod of next 4 nodes at level 2:

        ::

            >>> tree[0][0].get_manifest_payload_of_next_n_nodes_at_level(4, 2)
            [1, 2, 3, 4]

        Gets manifest paylaod of next 3 nodes at level 1:

        ::

            >>> tree[0][0].get_manifest_payload_of_next_n_nodes_at_level(3, 1)
            [1, 2, 3, 4, 5]

        Gets manifest paylaod of next node at level 0:

        ::

            >>> tree[0][0].get_manifest_payload_of_next_n_nodes_at_level(1, 0)
            [1, 2, 3, 4, 5, 6, 7]

        Gets manifest paylaod of next 4 nodes at level -1:

        ::

            >>> tree[0][0].get_manifest_payload_of_next_n_nodes_at_level(4, -1)
            [1, 2, 3, 4]

        Gets manifest paylaod of next 3 nodes at level -2:

        ::

            >>> tree[0][0].get_manifest_payload_of_next_n_nodes_at_level(3, -2)
            [1, 2, 3, 4, 5]

        Gets manifest paylaod of previous 4 nodes at level 2:

        ::

            >>> tree[-1][-1].get_manifest_payload_of_next_n_nodes_at_level(-4, 2)
            [6, 5, 4, 3]

        Gets manifest paylaod of previous 3 nodes at level 1:

        ::

            >>> tree[-1][-1].get_manifest_payload_of_next_n_nodes_at_level(-3, 1)
            [6, 5, 4, 3, 2]

        Gets manifest paylaod of previous node at level 0:

        ::

            >>> tree[-1][-1].get_manifest_payload_of_next_n_nodes_at_level(-1, 0)
            [6, 5, 4, 3, 2, 1, 0]

        Gets manifest paylaod of previous 4 nodes at level -1:

        ::

            >>> tree[-1][-1].get_manifest_payload_of_next_n_nodes_at_level(-4, -1)
            [6, 5, 4, 3]

        Gets manifest paylaod of previous 3 nodes at level -2:

        ::

            >>> tree[-1][-1].get_manifest_payload_of_next_n_nodes_at_level(-3, -2)
            [6, 5, 4, 3, 2]

        Trims first node if necessary.

        Returns list of arbitrary values.
        '''
        result = []
        nodes = self.get_next_n_nodes_at_level(n, level)
        for node in nodes:
            if 0 <= n:
                result.extend(node.manifest_payload)
            else:
                result.extend(reversed(node.manifest_payload))
        return result

    def get_next_n_complete_nodes_at_level(self, n, level):
        r'''Gets next `n` complete nodes at `level` from node.

        ..  container:: example

            Payload tree of length greater than ``1`` for examples
            with positive `n`:

            ::

                >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = datastructuretools.PayloadTree(sequence)

            Gets next 4 nodes at level 2:

            ::

                >>> tree[0][0].get_next_n_complete_nodes_at_level(4, 2)
                [PayloadTree(1), PayloadTree(2), PayloadTree(3), PayloadTree(4)]

            Gets next 3 nodes at level 1:

            ::

                >>> tree[0][0].get_next_n_complete_nodes_at_level(3, 1)
                [PayloadTree([1]), PayloadTree([2, 3]), PayloadTree([4, 5]), PayloadTree([6, 7])]

            Gets next 4 nodes at level -1:

            ::

                >>> tree[0][0].get_next_n_complete_nodes_at_level(4, -1)
                [PayloadTree(1), PayloadTree(2), PayloadTree(3), PayloadTree(4)]

            Gets next 3 nodes at level -2:

            ::

                >>> tree[0][0].get_next_n_complete_nodes_at_level(3, -2)
                [PayloadTree([1]), PayloadTree([2, 3]), PayloadTree([4, 5]), PayloadTree([6, 7])]

        ..  container:: example

            Payload tree of length greater than ``1`` for examples
            with negative `n`:

            ::

                >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = datastructuretools.PayloadTree(sequence)

            Gets previous 4 nodes at level 2:

            ::

                >>> tree[-1][-1].get_next_n_complete_nodes_at_level(-4, 2)
                [PayloadTree(6), PayloadTree(5), PayloadTree(4), PayloadTree(3)]

            Gets previous 3 nodes at level 1:

            ::

                >>> tree[-1][-1].get_next_n_complete_nodes_at_level(-3, 1)
                [PayloadTree([6]), PayloadTree([4, 5]), PayloadTree([2, 3]), PayloadTree([0, 1])]


            Gets previous 4 nodes at level -1:

            ::

                >>> tree[-1][-1].get_next_n_complete_nodes_at_level(-4, -1)
                [PayloadTree(6), PayloadTree(5), PayloadTree(4), PayloadTree(3)]

            Gets previous 3 nodes at level -2:

            ::

                >>> tree[-1][-1].get_next_n_complete_nodes_at_level(-3, -2)
                [PayloadTree([6]), PayloadTree([4, 5]), PayloadTree([2, 3]), PayloadTree([0, 1])]

        Trims first node if necessary.

        Returns list of nodes.
        '''
        return self._get_next_n_nodes_at_level_helper(
            n, level, nodes_must_be_complete=True)

    def get_next_n_nodes_at_level(self, n, level):
        r'''Gets next `n` nodes at `level` from node.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        Gets next 4 nodes at level 2:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(4, 2)
            [PayloadTree(1), PayloadTree(2), PayloadTree(3), PayloadTree(4)]

        Gets next 3 nodes at level 1:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(3, 1)
            [PayloadTree([1]), PayloadTree([2, 3]), PayloadTree([4, 5])]

        Gets next node at level 0:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(1, 0)
            [PayloadTree([[1], [2, 3], [4, 5], [6, 7]])]

        Gets next 4 nodes at level -1:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(4, -1)
            [PayloadTree(1), PayloadTree(2), PayloadTree(3), PayloadTree(4)]

        Gets next 3 nodes at level -2:

        ::

            >>> tree[0][0].get_next_n_nodes_at_level(3, -2)
            [PayloadTree([1]), PayloadTree([2, 3]), PayloadTree([4, 5])]

        Gets previous 4 nodes at level 2:

        ::

            >>> tree[-1][-1].get_next_n_nodes_at_level(-4, 2)
            [PayloadTree(6), PayloadTree(5), PayloadTree(4), PayloadTree(3)]

        Gets previous 3 nodes at level 1:

        ::

            >>> tree[-1][-1].get_next_n_nodes_at_level(-3, 1)
            [PayloadTree([6]), PayloadTree([4, 5]), PayloadTree([2, 3])]

        Gets previous node at level 0:

        ::

            >>> tree[-1][-1].get_next_n_nodes_at_level(-1, 0)
            [PayloadTree([[0, 1], [2, 3], [4, 5], [6]])]

        Gets previous 4 nodes at level -1:

        ::

            >>> tree[-1][-1].get_next_n_nodes_at_level(-4, -1)
            [PayloadTree(6), PayloadTree(5), PayloadTree(4), PayloadTree(3)]

        Gets previous 3 nodes at level -2:

        ::

            >>> tree[-1][-1].get_next_n_nodes_at_level(-3, -2)
            [PayloadTree([6]), PayloadTree([4, 5]), PayloadTree([2, 3])]

        Trims first node if necessary.

        Returns list of nodes.
        '''
        return self._get_next_n_nodes_at_level_helper(
            n, level, nodes_must_be_complete=False)

    def get_node_at_position(self, position):
        r'''Gets node at `position`.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree.get_node_at_position((2, 1))
            PayloadTree(5)

        Returns node.
        '''
        result = self
        for idx in position:
            result = result[idx]
        return result

    def get_position_of_descendant(self, descendant):
        r'''Gets position of `descendent` relative to node
        rather than relative to root.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[3].get_position_of_descendant(tree[3][0])
            (0,)

        Returns tuple of zero or more nonnegative integers.
        '''
        if descendant is self:
            return ()
        else:
            return descendant.position[len(self.position):]

    def index(self, node):
        r'''Index of `node`.

        ::

            >>> sequence = [0, 1, 2, 2, 3, 4]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> for node in tree:
            ...     node, tree.index(node)
            (PayloadTree(0), 0)
            (PayloadTree(1), 1)
            (PayloadTree(2), 2)
            (PayloadTree(2), 3)
            (PayloadTree(3), 4)
            (PayloadTree(4), 5)

        Returns nonnegative integer.
        '''
        for i, current_node in enumerate(self):
            if current_node is node:
                return i
        message = 'not in tree: {!r}.'
        message = message.format(node)
        raise ValueError(message)

    def is_at_level(self, level):
        r'''Is true when node is at `level` in containing tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree[1][1].is_at_level(-1)
            True

        Otherwise false:

        ::

            >>> tree[1][1].is_at_level(0)
            False

        Works for positive, negative and zero-valued `level`.

        Returns boolean.
        '''
        if (0 <= level and self.level == level) or \
            self.negative_level == level:
            return True
        else:
            return False

    def iterate_at_level(self, level, reverse=False):
        r'''Iterates tree at `level`.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        Left-to-right examples:

        ::

            >>> for x in tree.iterate_at_level(0): x
            ...
            PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])

        ::

            >>> for x in tree.iterate_at_level(1): x
            ...
            PayloadTree([0, 1])
            PayloadTree([2, 3])
            PayloadTree([4, 5])
            PayloadTree([6, 7])

        ::

            >>> for x in tree.iterate_at_level(2): x
            ...
            PayloadTree(0)
            PayloadTree(1)
            PayloadTree(2)
            PayloadTree(3)
            PayloadTree(4)
            PayloadTree(5)
            PayloadTree(6)
            PayloadTree(7)

        ::

            >>> for x in tree.iterate_at_level(-1): x
            ...
            PayloadTree(0)
            PayloadTree(1)
            PayloadTree(2)
            PayloadTree(3)
            PayloadTree(4)
            PayloadTree(5)
            PayloadTree(6)
            PayloadTree(7)

        ::

            >>> for x in tree.iterate_at_level(-2): x
            ...
            PayloadTree([0, 1])
            PayloadTree([2, 3])
            PayloadTree([4, 5])
            PayloadTree([6, 7])

        ::

            >>> for x in tree.iterate_at_level(-3): x
            ...
            PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])

        Right-to-left examples:

        ::

            >>> for x in tree.iterate_at_level(0, reverse=True): x
            ...
            PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])

        ::

            >>> for x in tree.iterate_at_level(1, reverse=True): x
            ...
            PayloadTree([6, 7])
            PayloadTree([4, 5])
            PayloadTree([2, 3])
            PayloadTree([0, 1])

        ::

            >>> for x in tree.iterate_at_level(2, reverse=True): x
            ...
            PayloadTree(7)
            PayloadTree(6)
            PayloadTree(5)
            PayloadTree(4)
            PayloadTree(3)
            PayloadTree(2)
            PayloadTree(1)
            PayloadTree(0)

        ::

            >>> for x in tree.iterate_at_level(-1, reverse=True): x
            ...
            PayloadTree(7)
            PayloadTree(6)
            PayloadTree(5)
            PayloadTree(4)
            PayloadTree(3)
            PayloadTree(2)
            PayloadTree(1)
            PayloadTree(0)

        ::

            >>> for x in tree.iterate_at_level(-2, reverse=True): x
            ...
            PayloadTree([6, 7])
            PayloadTree([4, 5])
            PayloadTree([2, 3])
            PayloadTree([0, 1])

        ::

            >>> for x in tree.iterate_at_level(-3, reverse=True): x
            ...
            PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])

        Returns node generator.
        '''
        for x in self.iterate_depth_first(reverse=reverse):
            if 0 <= level:
                if x.level == level:
                    yield x
            else:
                if x.negative_level == level:
                    yield x

    def iterate_depth_first(self, reverse=False):
        r'''Iterates tree depth-first.

        ..  container:: example

            **Example 1.** Iterate tree depth-first from left to right:

            ::

                >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = datastructuretools.PayloadTree(sequence)

            ::

                >>> for node in tree.iterate_depth_first(): node
                ...
                PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])
                PayloadTree([0, 1])
                PayloadTree(0)
                PayloadTree(1)
                PayloadTree([2, 3])
                PayloadTree(2)
                PayloadTree(3)
                PayloadTree([4, 5])
                PayloadTree(4)
                PayloadTree(5)
                PayloadTree([6, 7])
                PayloadTree(6)
                PayloadTree(7)

        ..  container::

            **Example 2.** Iterate tree depth-first from right to left:

            ::

                >>> for node in tree.iterate_depth_first(reverse=True): node
                ...
                PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])
                PayloadTree([6, 7])
                PayloadTree(7)
                PayloadTree(6)
                PayloadTree([4, 5])
                PayloadTree(5)
                PayloadTree(4)
                PayloadTree([2, 3])
                PayloadTree(3)
                PayloadTree(2)
                PayloadTree([0, 1])
                PayloadTree(1)
                PayloadTree(0)

        Returns node generator.
        '''
        yield self
        iterable_self = self
        if reverse:
            iterable_self = reversed(self)
        for x in iterable_self:
            for y in x.iterate_depth_first(reverse=reverse):
                yield y

    def iterate_payload(self, reverse=False):
        r'''Iterates payload of tree.

        ..  container:: example

            **Example 1.** Iterates payload from left to right:

            ::

                >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = datastructuretools.PayloadTree(sequence)

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

        ..  container:: example

            **Example 2.** Iterates payload from right to left:

            ::

                >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
                >>> tree = datastructuretools.PayloadTree(sequence)

            ::

                >>> for element in tree.iterate_payload(reverse=True):
                ...     element
                ...
                7
                6
                5
                4
                3
                2
                1
                0

        Returns payload generator.
        '''
        for leaf_node in self.iterate_at_level(-1, reverse=reverse):
            yield leaf_node.payload

    def remove_node(self, node):
        r'''Removes `node` from tree.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree.remove_node(tree[1])

        ::

            >>> tree
            PayloadTree([[0, 1], [4, 5], [6, 7]])

        Returns none.
        '''
        node.parent._children.remove(node)
        node.parent = None

    def remove_to_root(self, reverse=False):
        r'''Removes node and all nodes left of node to root.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]

        ::

            >>> tree = datastructuretools.PayloadTree(sequence)
            >>> tree[0][0].remove_to_root()
            >>> tree
            PayloadTree([[1], [2, 3], [4, 5], [6, 7]])

        ::

            >>> tree = datastructuretools.PayloadTree(sequence)
            >>> tree[0][1].remove_to_root()
            >>> tree
            PayloadTree([[2, 3], [4, 5], [6, 7]])

        ::

            >>> tree = datastructuretools.PayloadTree(sequence)
            >>> tree[1].remove_to_root()
            >>> tree
            PayloadTree([[4, 5], [6, 7]])

        Modifies in-place to root.

        Returns none.
        '''
        ## trim left-siblings of self and self
        parent = self.parent
        if reverse:
            iterable_parent = reversed(parent)
        else:
            iterable_parent = parent[:]
        for sibling in iterable_parent:
            sibling.parent.remove_node(sibling)
            ## break and do not remove siblings to right of self
            if sibling is self:
                break
        ## trim parentage
        for node in parent.improper_parentage:
            if node.parent is not None:
                iterable_parent = node.parent[:]
                if reverse:
                    iterable_parent = reversed(node.parent)
                else:
                    iterable_parent = node.parent[:]
                for sibling in iterable_parent:
                    if sibling is node:
                        # remove node now if it was emptied earlier
                        if not len(sibling):
                            sibling.parent.remove_node(sibling)
                        break
                    else:
                        sibling.parent.remove_node(sibling)

    def to_nested_lists(self):
        r'''Changes tree to nested lists.

        ::

            >>> sequence = [[0, 1], [2, 3], [4, 5], [6, 7]]
            >>> tree = datastructuretools.PayloadTree(sequence)

        ::

            >>> tree
            PayloadTree([[0, 1], [2, 3], [4, 5], [6, 7]])

        ::

            >>> tree.to_nested_lists()
            [[0, 1], [2, 3], [4, 5], [6, 7]]

        Returns list of lists.
        '''
        if self.payload is not None:
            message = 'leaf node is not iterable.'
            raise TypeError(message)
        else:
            result = []
            for child in self._noncyclic_children:
                if child.payload is not None:
                    result.append(child.payload)
                else:
                    result.append(child.to_nested_lists())
            return result