import copy
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class TreeNode(AbjadObject):
    '''A node in a generalized tree.

    Return `TreeNode` instance.
    '''

    ### INITIALIZER ###

    def __init__(self, name=None):
        self._name = None
        self._parent = None    
        self.name = name

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        return type(self)(
            *[copy.deepcopy(x) for x in self.__getnewargs__()]
            )

    __deepcopy__ = __copy__

    def __eq__(self, other):
        if type(self) == type(other):
            return True
        return False

    def __getnewargs__(self):
        return self._positional_argument_values + self._keyword_argument_values

    def __getstate__(self):
        state = {}
        for name in self._positional_argument_names:
            state['_' + name] = getattr(self, name)
        for name in self._keyword_argument_names:
            state['_' + name] = getattr(self, name)
        state['_parent'] = self._parent
        return state

    def __ne__(self, other):
        return not self.__eq__(other)

    def __repr__(self):

        def format_mapping(name, value):
            if not value:
                return None
            result = ['\t{}={{'.format(name)]
            items = sorted(value.items())
            if 1 < len(items):
                for item in items[:-1]:
                    result.append('\t\t{!r}: {!r},'.format(*item))
            result.append('\t\t{!r}: {!r}'.format(*items[-1]))
            result.append('\t\t}')
            return result

        def format_tuple(name, value):
            if not value:
                return None
            result=['\t{}=('.format(name)]
            items = [repr(x).splitlines() for x in value]
            if 1 < len(items):
                for item in items[:-1]:
                    result.extend('\t\t' + x for x in item[:-1])
                    result.append('\t\t' + item[-1] + ',')
                result.extend('\t\t' + x for x in items[-1])
            else:
                result.extend('\t\t' + x for x in items[0][:-1])
                result.append('\t\t' + items[0][-1] + ',')
            result.append('\t\t)')
            return result

        def format_other(name, value):
            if value is None:
                return None
            item = repr(value).splitlines()
            result = ['\t{}={}'.format(name, item[0])]
            result.extend('\t\t' + x for x in item[1:])
            return result

        attr_pieces = []
        for name in self._keyword_argument_names:
            value = getattr(self, name)
            if isinstance(value, (list, tuple)):
                attr_piece = format_tuple(name, value)
            elif isinstance(value, dict):
                attr_piece = format_mapping(name, value)
            else:
                attr_piece = format_other(name, value)
            if attr_piece is not None:
                attr_pieces.append(attr_piece)

        if not attr_pieces:
            return '{}()'.format(self._class_name)

        result = ['{}('.format(self._class_name)]
        if 1 < len(attr_pieces):
            for attr_piece in attr_pieces[:-1]:
                attr_piece[-1] += ','
                result.extend(attr_piece)
        result.extend(attr_pieces[-1]) 
        result.append('\t)')
        return '\n'.join(result)

    def __setstate__(self, state):
        for key, value in state.iteritems():
            setattr(self, key, value)

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

        name_dictionary = {}
        if hasattr(self, '_named_children'):
            for name, children in self._named_children.iteritems():
                name_dictionary[name] = copy.copy(children)
        if hasattr(self, 'name') and self.name is not None:
            if self.name not in name_dictionary:
                name_dictionary[self.name] = set([])
            name_dictionary[self.name].add(self)

        if self._parent is not None and name_dictionary:
            for parent in self.proper_parentage_parentage:
                named_children = parent._named_children
                for name in name_dictionary:
                    for node in name_dictionary[name]:
                        named_children[name].remove(node)
                    if not named_children[name]:
                        del named_children[name]

        if self._parent is not None:
            index = self._parent.index(self)
            self._parent._children.pop(index)
        self._parent = new_parent

        if new_parent is not None and name_dictionary:
            for parent in self.proper_parentage:
                named_children = parent._named_children
                for name in name_dictionary:
                    if name in named_children:
                        named_children[name].update(name_dictionary[name])
                    else:
                        named_children[name] = copy.copy(name_dictionary[name])

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
            ...     print 'DEPTH: {}'.format(depth)
            ...     for node in inventory[depth]:
            ...         print node.name 
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

        Return tuple of `TreeNode` instances.
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

        Return `TreeNode` instance.
        '''
        return self._parent

    @property
    def proper_parentage(self):
        '''The proper parentage of a node in a rhythm-tree, being the 
        sequence of node beginning with the node's immediate parent and
        ending with the root node of the tree:

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

        Return tuple of `TreeNode` instances.
        '''
        return self.improper_parentage[1:]

    @property
    def root(self):
        '''The root node of the tree: that node in the tree which has
        no parent:

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

        Return `TreeNode` instance.
        '''
        node = self
        while node.parent is not None:
            node = node.parent
        return node

    ### READ/WRITE PROPERTIES ###

    @apply
    def name():
        def fget(self):
            return self._name
        def fset(self, arg):
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
        return property(**locals())

