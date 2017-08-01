# -*- coding: utf-8 -*-
from abjad.tools import systemtools
from abjad.tools.datastructuretools.TreeNode import TreeNode


class TreeContainer(TreeNode):
    r'''Tree container.

    ::

        >>> import abjad

    Inner node in a generalized tree data structure.

    ::

        >>> a = abjad.TreeContainer()
        >>> a
        TreeContainer()

    ::

        >>> b = abjad.TreeNode()
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

    def __contains__(self, argument):
        r'''True if argument is in container. Otherwise false:

        ::

            >>> container = abjad.TreeContainer()
            >>> a = abjad.TreeNode()
            >>> b = abjad.TreeNode()
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
            if x is argument:
                return True
        return False

    def __delitem__(self, i):
        r'''Deletes node `i` in tree container.

        ::

            >>> container = abjad.TreeContainer()
            >>> leaf = abjad.TreeNode()

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

    def __eq__(self, argument):
        r'''Is true when container equals `argument`. Otherwise false.

        ..  container:: example

            >>> tree_container_1 = abjad.TreeContainer([])
            >>> tree_container_2 = abjad.TreeContainer([])

        ::

            >>> format(tree_container_1) == format(tree_container_2)
            True

        ::

            >>> tree_container_1 != tree_container_2
            True

        ..  container:: example

            >>> tree_container_1 = abjad.TreeContainer([abjad.TreeNode()])
            >>> tree_container_2 = abjad.TreeContainer([abjad.TreeNode()])

        ::

            >>> format(tree_container_1) == format(tree_container_2)
            True

        ::

            >>> tree_container_1 != tree_container_2
            True

        ..  container:: example

            >>> tree_container_1 = abjad.TreeContainer([])
            >>> tree_container_2 = abjad.TreeContainer([abjad.TreeNode()])
            >>> tree_container_3 = abjad.TreeContainer([
            ...    abjad.TreeNode(),
            ...    abjad.TreeNode()
            ...    ])

        ::

            >>> format(tree_container_1) != format(tree_container_2)
            True

        ::

            >>> tree_container_1 != tree_container_2
            True

        ::

            >>> tree_container_1 != tree_container_3
            True

        ::

            >>> tree_container_2 != tree_container_3
            True

        Returns true, false or none.
        '''
        return super(TreeContainer, self).__eq__(argument)

    def __getitem__(self, argument):
        r'''Gets item or slice identified by `argument`.

        ::

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeNode()
            >>> c = abjad.TreeContainer()
            >>> d = abjad.TreeNode()
            >>> e = abjad.TreeNode()
            >>> f = abjad.TreeNode()

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

            >>> foo = abjad.TreeContainer(name='foo')
            >>> bar = abjad.TreeContainer(name='bar')
            >>> baz = abjad.TreeNode(name='baz')
            >>> quux = abjad.TreeNode(name='quux')

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
        if isinstance(argument, (int, slice)):
            return self._children.__getitem__(argument)
        elif isinstance(argument, str):
            children = self._named_children.__getitem__(argument)
            if 1 == len(children):
                return tuple(children)[0]
        raise ValueError(repr(argument))

    def __hash__(self):
        r'''Hashes tree container.

        Returns number.
        '''
        return super(TreeContainer, self).__hash__()

    def __iter__(self):
        r'''Iterates tree container.

        Yields children of tree container.
        '''
        for child in self._children:
            yield child

    def __len__(self):
        r'''Returns nonnegative integer number of nodes in container.

        ..  container:: example

            ::

                >>> leaf_a = abjad.TreeNode()
                >>> leaf_b = abjad.TreeNode()
                >>> leaf_c = abjad.TreeNode()
                >>> subcontainer = abjad.TreeContainer([leaf_b, leaf_c])
                >>> leaf_d = abjad.TreeNode()
                >>> container = abjad.TreeContainer([
                ...     leaf_a,
                ...     subcontainer,
                ...     leaf_d,
                ...     ])

            ::

                >>> len(container)
                3

        '''
        return len(self._children)

    def __setitem__(self, i, argument):
        r'''Sets `argument` in self at nonnegative integer index `i`, or set `argument`
        in self at slice i. Replace contents of `self[i]` with `argument`.
        Attach parentage to contents of `argument`, and detach parentage
        of any replaced nodes:

        ::

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeNode()
            >>> c = abjad.TreeNode()

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
            assert isinstance(argument, self._node_class)
            old = self[i]
            assert argument not in proper_parentage
            old._set_parent(None)
            argument._set_parent(self)
            self._children.insert(i, argument)
        else:
            if isinstance(argument, TreeContainer):
                # Prevent mutating while iterating by copying.
                argument = argument[:]
            assert all(isinstance(x, self._node_class) for x in argument)
            if i.start == i.stop and i.start is not None \
                and i.stop is not None and i.start <= -len(self):
                start, stop = 0, 0
            else:
                start, stop, stride = i.indices(len(self))
            old = self[start:stop]
            for node in argument:
                assert node not in proper_parentage
            for node in old:
                node._set_parent(None)
            for node in argument:
                node._set_parent(self)
            self._children.__setitem__(slice(start, start), argument)
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

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeNode()
            >>> c = abjad.TreeNode()

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

    def extend(self, argument):
        r'''Extendes `argument` against tree container.

        ::

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeNode()
            >>> c = abjad.TreeNode()

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
            argument
            )

    def index(self, node):
        r'''Indexes `node` in tree container.

        ::

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeNode()
            >>> c = abjad.TreeNode()

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

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeNode()
            >>> c = abjad.TreeNode()
            >>> d = abjad.TreeNode()

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

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeNode()
            >>> c = abjad.TreeNode()

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

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeNode()
            >>> c = abjad.TreeNode()

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

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeContainer()
            >>> c = abjad.TreeNode()
            >>> d = abjad.TreeNode()
            >>> e = abjad.TreeContainer()

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

            >>> a = abjad.TreeContainer(name='a')
            >>> b = abjad.TreeContainer(name='b')
            >>> c = abjad.TreeNode(name='c')
            >>> d = abjad.TreeNode(name='d')
            >>> e = abjad.TreeContainer(name='e')

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
                try:
                    children = child.children
                    has_children = True
                except AttributeError:
                    has_children = False
                if not has_children:
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

            >>> a = abjad.TreeContainer()
            >>> b = abjad.TreeContainer()
            >>> c = abjad.TreeNode()
            >>> d = abjad.TreeNode()
            >>> e = abjad.TreeContainer()

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
