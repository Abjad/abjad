# -*- coding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools.datastructuretools.TreeNode import TreeNode


class TreeContainer(TreeNode):
    r'''A tree container.

    Inner node in a generalized tree data structure.

    ::

        >>> a = datastructuretools.TreeContainer()
        >>> a
        TreeContainer()

    ::

        >>> b = datastructuretools.TreeNode()
        >>> a.append(b)
        >>> a
        TreeContainer(
            children=(
                TreeNode(),
                )
            )

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_children',
        '_named_children',
        )

    ### INITIALIZER ###

    def __init__(self, children=None, name=None):
        TreeNode.__init__(self, name=name)
        self._children = []
        self._named_children = {}
        if children is None:
            pass
        elif isinstance(children, (list, tuple)):
            self.extend(children)
        else:
            message = 'can not instantiate {} with {!r}.'
            message = message.format(type(self), children)
            raise ValueError(message)

    ### SPECIAL METHODS ###

    def __contains__(self, expr):
        r'''True if expr is in container. Otherwise false:

        ::

            >>> container = datastructuretools.TreeContainer()
            >>> a = datastructuretools.TreeNode()
            >>> b = datastructuretools.TreeNode()
            >>> container.append(a)

        ::

            >>> a in container
            True

        ::

            >>> b in container
            False

        Returns true or false.
        '''
        for x in self._children:
            if x is expr:
                return True
        return False

    def __delitem__(self, i):
        r'''Deletes node `i` in tree container.

        ::

            >>> container = datastructuretools.TreeContainer()
            >>> leaf = datastructuretools.TreeNode()

        ::

            >>> container.append(leaf)
            >>> container.children == (leaf,)
            True

        ::

            >>> leaf.parent is container
            True

        ::

            >>> del(container[0])

        ::

            >>> container.children == ()
            True

        ::

            >>> leaf.parent is None
            True

        Return `None`.
        '''
        nodes = self[i]
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            node._set_parent(None)
        self._mark_entire_tree_for_later_update()

    def __getitem__(self, i):
        r'''Gets node `i` in tree container.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeNode()
            >>> c = datastructuretools.TreeContainer()
            >>> d = datastructuretools.TreeNode()
            >>> e = datastructuretools.TreeNode()
            >>> f = datastructuretools.TreeNode()

        ::

            >>> a.extend([b, c, f])
            >>> c.extend([d, e])

        ::

            >>> a[0] is b
            True

        ::

            >>> a[1] is c
            True

        ::

            >>> a[2] is f
            True

        If `i` is a string, the container will attempt to
        return the single child node, at any depth, whose
        `name` matches `i`:

        ::

            >>> foo = datastructuretools.TreeContainer(name='foo')
            >>> bar = datastructuretools.TreeContainer(name='bar')
            >>> baz = datastructuretools.TreeNode(name='baz')
            >>> quux = datastructuretools.TreeNode(name='quux')

        ::

            >>> foo.append(bar)
            >>> bar.extend([baz, quux])

        ::

            >>> foo['bar'] is bar
            True

        ::

            >>> foo['baz'] is baz
            True

        ::

            >>> foo['quux'] is quux
            True

        Return `TreeNode` instance.
        '''
        if isinstance(i, (int, slice)):
            return self._children[i]
        elif isinstance(i, str):
            children = self._named_children[i]
            if 1 == len(children):
                return tuple(children)[0]
        raise ValueError(repr(i))

    def __iter__(self):
        r'''Iterates tree container.

        Yields children of tree container.
        '''
        for child in self._children:
            yield child

    def __len__(self):
        r'''Returns nonnegative integer number of nodes in container.
        '''
        return len(self._children)

    def __setitem__(self, i, expr):
        r'''Sets `expr` in self at nonnegative integer index `i`, or set `expr`
        in self at slice i. Replace contents of `self[i]` with `expr`.
        Attach parentage to contents of `expr`, and detach parentage
        of any replaced nodes:

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeNode()
            >>> c = datastructuretools.TreeNode()

        ::

            >>> a.append(b)
            >>> b.parent is a
            True

        ::

            >>> a.children == (b,)
            True

        ::

            >>> a[0] = c

        ::

            >>> c.parent is a
            True


        ::

            >>> b.parent is None
            True

        ::

            >>> a.children == (c,)
            True

        Returns none.
        '''
        proper_parentage = self.proper_parentage

        if isinstance(i, int):
            assert isinstance(expr, self._node_class)
            old = self[i]
            assert expr not in proper_parentage
            old._set_parent(None)
            expr._set_parent(self)
            self._children.insert(i, expr)
        else:
            if isinstance(expr, TreeContainer):
                # Prevent mutating while iterating by copying.
                expr = expr[:]
            assert all(isinstance(x, self._node_class) for x in expr)
            if i.start == i.stop and i.start is not None \
                and i.stop is not None and i.start <= -len(self):
                start, stop = 0, 0
            else:
                start, stop, stride = i.indices(len(self))
            old = self[start:stop]
            for node in expr:
                assert node not in proper_parentage
            for node in old:
                node._set_parent(None)
            for node in expr:
                node._set_parent(self)
            self._children.__setitem__(slice(start, start), expr)
        self._mark_entire_tree_for_later_update()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = list(agent.signature_keyword_names)
        template_names = names[:]
        for name in ('children',):
            if not getattr(self, name, None) and name in names:
                names.remove(name)
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            storage_format_kwargs_names=names,
            template_names=template_names,
            )
    ### PUBLIC METHODS ###

    def append(self, node):
        r'''Appends `node` to tree container.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeNode()
            >>> c = datastructuretools.TreeNode()

        ::

            >>> a
            TreeContainer()

        ::

            >>> a.append(b)
            >>> a
            TreeContainer(
                children=(
                    TreeNode(),
                    )
                )

        ::

            >>> a.append(c)
            >>> a
            TreeContainer(
                children=(
                    TreeNode(),
                    TreeNode(),
                    )
                )

        Returns none.
        '''
        self.__setitem__(
            slice(len(self), len(self)),
            [node]
            )

    def extend(self, expr):
        r'''Extendes `expr` against tree container.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeNode()
            >>> c = datastructuretools.TreeNode()

        ::

            >>> a
            TreeContainer()

        ::

            >>> a.extend([b, c])
            >>> a
            TreeContainer(
                children=(
                    TreeNode(),
                    TreeNode(),
                    )
                )

        Returns none.
        '''
        self.__setitem__(
            slice(len(self), len(self)),
            expr
            )

    def index(self, node):
        r'''Indexes `node` in tree container.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeNode()
            >>> c = datastructuretools.TreeNode()

        ::

            >>> a.extend([b, c])

        ::

            >>> a.index(b)
            0

        ::

            >>> a.index(c)
            1

        Returns nonnegative integer.
        '''
        for i, element in enumerate(self._children):
            if element is node:
                return i
        else:
            message = 'node {!r} not in {!r}.'
            message = message.format(node, self)
            raise ValueError(message)

    def insert(self, i, node):
        r'''Insert `node` in tree container at index `i`.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeNode()
            >>> c = datastructuretools.TreeNode()
            >>> d = datastructuretools.TreeNode()

        ::

            >>> a.extend([b, c])

        ::

            >>> a
            TreeContainer(
                children=(
                    TreeNode(),
                    TreeNode(),
                    )
                )

        ::

            >>> a.insert(1, d)

        ::

            >>> a
            TreeContainer(
                children=(
                    TreeNode(),
                    TreeNode(),
                    TreeNode(),
                    )
                )


        Return `None`.
        '''
        self.__setitem__(
            slice(i, i),
            [node]
            )

    def pop(self, i=-1):
        r'''Pops node `i` from tree container.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeNode()
            >>> c = datastructuretools.TreeNode()

        ::

            >>> a.extend([b, c])

        ::

            >>> a
            TreeContainer(
                children=(
                    TreeNode(),
                    TreeNode(),
                    )
                )

        ::

            >>> node = a.pop()

        ::

            >>> node == c
            True

        ::

            >>> a
            TreeContainer(
                children=(
                    TreeNode(),
                    )
                )

        Returns node.
        '''
        node = self[i]
        del(self[i])
        return node

    def remove(self, node):
        r'''Remove `node` from tree container.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeNode()
            >>> c = datastructuretools.TreeNode()

        ::

            >>> a.extend([b, c])

        ::

            >>> a
            TreeContainer(
                children=(
                    TreeNode(),
                    TreeNode(),
                    )
                )

        ::

            >>> a.remove(b)

        ::

            >>> a
            TreeContainer(
                children=(
                    TreeNode(),
                    )
                )

        Returns none.
        '''
        i = self.index(node)
        del(self[i])

    ### PRIVATE PROPERTIES ###

    @property
    def _leaf_class(self):
        return TreeNode

    @property
    def _node_class(self):
        return TreeNode

    ### PUBLIC PROPERTIES ###

    @property
    def children(self):
        r'''Children of tree container.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeContainer()
            >>> c = datastructuretools.TreeNode()
            >>> d = datastructuretools.TreeNode()
            >>> e = datastructuretools.TreeContainer()

        ::

            >>> a.extend([b, c])
            >>> b.extend([d, e])

        ::

            >>> a.children == (b, c)
            True

        ::

            >>> b.children == (d, e)
            True

        ::

            >>> e.children == ()
            True

        Returns tuple of tree nodes.
        '''
        return tuple(self._children)

    @property
    def leaves(self):
        r'''Leaves of tree container.

        ::

            >>> a = datastructuretools.TreeContainer(name='a')
            >>> b = datastructuretools.TreeContainer(name='b')
            >>> c = datastructuretools.TreeNode(name='c')
            >>> d = datastructuretools.TreeNode(name='d')
            >>> e = datastructuretools.TreeContainer(name='e')

        ::

            >>> a.extend([b, c])
            >>> b.extend([d, e])

        ::

            >>> for leaf in a.leaves:
            ...     print(leaf.name)
            ...
            d
            e
            c

        Returns tuple.
        '''
        def recurse(node):
            result = []
            for child in node:
                if not hasattr(child, 'children'):
                    if isinstance(child, self._leaf_class):
                        result.append(child)
                elif not child.children:
                    if isinstance(child, self._leaf_class):
                        result.append(child)
                else:
                    result.extend(recurse(child))
            return result
        return tuple(recurse(self))

    @property
    def nodes(self):
        r'''The collection of tree nodes produced by iterating tree container
        depth-first.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeContainer()
            >>> c = datastructuretools.TreeNode()
            >>> d = datastructuretools.TreeNode()
            >>> e = datastructuretools.TreeContainer()

        ::

            >>> a.extend([b, c])
            >>> b.extend([d, e])

        ::

            >>> nodes = a.nodes
            >>> len(nodes)
            5

        ::

            >>> nodes[0] is a
            True

        ::

            >>> nodes[1] is b
            True

        ::

            >>> nodes[2] is d
            True

        ::

            >>> nodes[3] is e
            True

        ::

            >>> nodes[4] is c
            True

        Returns tuple.
        '''
        def recurse(container):
            result = []
            for child in container.children:
                result.append(child)
                if isinstance(child, datastructuretools.TreeContainer):
                    result.extend(recurse(child))
            return result
        from abjad.tools import datastructuretools
        result = [self] + recurse(self)
        return tuple(result)
