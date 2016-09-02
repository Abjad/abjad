# -*- coding: utf-8 -*-
import copy
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadObject


class TreeNode(AbjadObject):
    r'''A node.

    Node in a generalized tree.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_name',
        '_parent',
        )

    ### INITIALIZER ###

    def __init__(self, name=None):
        self._name = None
        self._parent = None
        self.name = name

    ### SPECIAL METHODS ###

    def __copy__(self):
        r'''Copies tree node.
        '''
        import copy
        agent = systemtools.StorageFormatAgent(self)
        arguments = []
        for value in agent.get_template_dict().values():
            if isinstance(value, tuple):
                value = tuple(copy.copy(_) for _ in value)
            else:
                value = copy.copy(value)
            arguments.append(value)
        return type(self)(*arguments)

    ### PRIVATE METHODS ###

    def _cache_named_children(self):
        name_dictionary = {}
        if hasattr(self, '_named_children'):
            for name, children in self._named_children.items():
                name_dictionary[name] = copy.copy(children)
        if hasattr(self, 'name') and self.name is not None:
            if self.name not in name_dictionary:
                name_dictionary[self.name] = set([])
            name_dictionary[self.name].add(self)
        return name_dictionary

    def _get_format_specification(self):
        agent = systemtools.StorageFormatAgent(self)
        names = agent.signature_names
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=True,
            template_names=names,
            )

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

    def _remove_from_parent(self):
        if self._parent is not None:
            index = self._parent.index(self)
            self._parent._children.pop(index)

    def _remove_named_children_from_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self.proper_parentage:
                named_children = parent._named_children
                for name in name_dictionary:
                    for node in name_dictionary[name]:
                        named_children[name].remove(node)
                    if not named_children[name]:
                        del named_children[name]

    def _restore_named_children_to_parentage(self, name_dictionary):
        if self._parent is not None and name_dictionary:
            for parent in self.proper_parentage:
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].update(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

    def _set_parent(self, new_parent):
        named_children = self._cache_named_children()
        self._remove_named_children_from_parentage(named_children)
        self._remove_from_parent()
        self._parent = new_parent
        self._restore_named_children_to_parentage(named_children)
        self._mark_entire_tree_for_later_update()

    ### PRIVATE PROPERTIES ###

    @property
    def _state_flag_names(self):
        return ()

    ### PUBLIC PROPERTIES ###

    @property
    def depth(self):
        r'''The depth of a node in a rhythm-tree structure.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeContainer()
            >>> c = datastructuretools.TreeNode()
            >>> a.append(b)
            >>> b.append(c)

        ::

            >>> a.depth
            0

        ::

            >>> a[0].depth
            1

        ::

            >>> a[0][0].depth
            2

        Returns int.
        '''
        node = self
        depth = 0
        while node.parent is not None:
            depth += 1
            node = node.parent
        return depth

    @property
    def depthwise_inventory(self):
        r'''A dictionary of all nodes in a rhythm-tree, organized by their
        depth relative the root node.

        ::

            >>> a = datastructuretools.TreeContainer(name='a')
            >>> b = datastructuretools.TreeContainer(name='b')
            >>> c = datastructuretools.TreeContainer(name='c')
            >>> d = datastructuretools.TreeContainer(name='d')
            >>> e = datastructuretools.TreeContainer(name='e')
            >>> f = datastructuretools.TreeContainer(name='f')
            >>> g = datastructuretools.TreeContainer(name='g')

        ::

            >>> a.extend([b, c])
            >>> b.extend([d, e])
            >>> c.extend([f, g])

        ::

            >>> inventory = a.depthwise_inventory
            >>> for depth in sorted(inventory):
            ...     print('DEPTH: {}'.format(depth))
            ...     for node in inventory[depth]:
            ...         print(node.name)
            ...
            DEPTH: 0
            a
            DEPTH: 1
            b
            c
            DEPTH: 2
            d
            e
            f
            g

        Returns dictionary.
        '''
        def recurse(node):
            if node.depth not in inventory:
                inventory[node.depth] = []
            inventory[node.depth].append(node)
            if hasattr(node, 'children'):
                for child in node.children:
                    recurse(child)
        inventory = {}
        recurse(self)
        return inventory

    @property
    def graph_order(self):
        r'''Graph order of tree node.

        Returns tuple.
        '''
        from abjad.tools import sequencetools
        order = []
        for parent, child in sequencetools.iterate_sequence_nwise(
            reversed(self.improper_parentage)):
            order.append(parent.index(child))
        return tuple(order)

    @property
    def improper_parentage(self):
        r'''The improper parentage of a node in a rhythm-tree, being the
        sequence of node beginning with itself and ending with the root node
        of the tree.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeContainer()
            >>> c = datastructuretools.TreeNode()

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

        Returns tuple of tree nodes.
        '''
        node = self
        parentage = [node]
        while node.parent is not None:
            node = node.parent
            parentage.append(node)
        return tuple(parentage)

    @property
    def parent(self):
        r'''Parent of tree node.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeContainer()
            >>> c = datastructuretools.TreeNode()

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

        Returns tree node.
        '''
        return self._parent

    @property
    def proper_parentage(self):
        r'''The proper parentage of a node in a rhythm-tree, being the
        sequence of node beginning with the node's immediate parent and
        ending with the root node of the tree.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeContainer()
            >>> c = datastructuretools.TreeNode()

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

        Returns tuple of tree nodes.
        '''
        return self.improper_parentage[1:]

    @property
    def root(self):
        r'''The root node of the tree: that node in the tree which has
        no parent.

        ::

            >>> a = datastructuretools.TreeContainer()
            >>> b = datastructuretools.TreeContainer()
            >>> c = datastructuretools.TreeNode()

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

        Returns tree node.
        '''
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    ### PUBLIC PROPERTIES ###

    @property
    def name(self):
        r'''Named of tree node.

        Returns string.
        '''
        return self._name

    @name.setter
    def name(self, arg):
        assert isinstance(arg, (str, type(None)))
        old_name = self._name
        for parent in self.proper_parentage:
            named_children = parent._named_children
            if old_name is not None:
                named_children[old_name].remove(self)
                if not named_children[old_name]:
                    del named_children[old_name]
            if arg is not None:
                if arg not in named_children:
                    named_children[arg] = set([self])
                else:
                    named_children[arg].add(self)
        self._name = arg
