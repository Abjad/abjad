import copy
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import tietools
from abjad.tools import tuplettools
from abjad.tools.rhythmtreetools.RhythmTreeNode import RhythmTreeNode


class RhythmTreeContainer(RhythmTreeNode):
    r'''A container node in a rhythm tree structure:

    ::

        >>> container = rhythmtreetools.RhythmTreeContainer(duration=1, children=[])
        >>> container
        RhythmTreeContainer(
            duration=1
            )

    Similar to Abjad containers, `RhythmTreeContainer` supports a list interface,
    and can be appended, extended, indexed and so forth by other `RhythmTreeNode`
    subclasses:

    ::

        >>> leaf_a = rhythmtreetools.RhythmTreeLeaf(1)
        >>> leaf_b = rhythmtreetools.RhythmTreeLeaf(2)
        >>> container.extend([leaf_a, leaf_b])
        >>> container
        RhythmTreeContainer(
            children=(
                RhythmTreeLeaf(
                    duration=1,
                    is_pitched=True,
                    ),
                RhythmTreeLeaf(
                    duration=2,
                    is_pitched=True,
                    ),
            ),
            duration=1
            )

    ::

        >>> another_container = rhythmtreetools.RhythmTreeContainer(2)
        >>> another_container.append(rhythmtreetools.RhythmTreeLeaf(3))
        >>> another_container.append(container[1])
        >>> container.append(another_container)
        >>> container
        RhythmTreeContainer(
            children=(
                RhythmTreeLeaf(
                    duration=1,
                    is_pitched=True,
                    ),
                RhythmTreeContainer(
                    children=(
                        RhythmTreeLeaf(
                            duration=3,
                            is_pitched=True,
                            ),
                        RhythmTreeLeaf(
                            duration=2,
                            is_pitched=True,
                            ),
                    ),
                    duration=2
                    ),
            ),
            duration=1
            )

    Call `RhythmTreeContainer` with a duration to generate a tuplet structure:

    ::

        >>> container((1, 4))
        [FixedDurationTuplet(1/4, [c'8, {@ 5:4 c'8., c'8 @}])]

    ::

        >>> f(_[0])
        \times 2/3 {
            c'8
            \times 4/5 {
                c'8.
                c'8
            }
        }

    Returns `RhythmTreeContainer` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_children', '_duration', '_offset', '_offsets_are_current', '_parent')

    ### INITIALIZER ###

    def __init__(self, duration=1, children=None):
        RhythmTreeNode.__init__(self, duration)
        self._children = []
        if isinstance(children, type(None)):
            pass
        elif isinstance(children, (list, str, tuple)):
            self.extend(children)
        else:
            raise ValueError('Cannot instantiate {} with {!r}.'.format(type(self), children))

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        '''Concatenate containers self and expr. The operation c = a + b
        returns a new RhythmTreeContainer c with the content of both a and b,
        and a duration equal to the sum of the durations of a and b. The
        operation is non-commutative: the content of the first operand will be
        placed before the content of the second operand:

        ::

            >>> a = rhythmtreetools.RhythmTreeParser()('(1 (1 1 1))')[0]
            >>> b = rhythmtreetools.RhythmTreeParser()('(2 (3 4))')[0]

        ::

            >>> c = a + b

        ::

            >>> c.duration
            3

        ::

            >>> c
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=1,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=1,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=1,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=4,
                        is_pitched=True,
                        ),
                ),
                duration=3
                )

        '''
        from abjad.tools.rhythmtreetools.RhythmTreeParser import RhythmTreeParser
        if isinstance(expr, str):
            expr = RhythmTreeParser()(expr)
            assert 1 == len(expr) and isinstance(expr[0], type(self))
            expr = expr[0]
        container = type(self)(self.duration + expr.duration)
        container.extend(self[:])
        container.extend(expr[:])
        return container

    def __call__(self, pulse_duration):
        '''Generate Abjad score components:

        ::

            >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

        ::

            >>> tree((1, 4))
            [FixedDurationTuplet(1/4, [c'16, {@ 3:2 c'16, c'16, c'16 @}, c'8])]

        Return sequence of components.
        '''
        pulse_duration = durationtools.Duration(pulse_duration)
        assert 0 < pulse_duration
        def recurse(node, duration):
            tuplet = tuplettools.FixedDurationTuplet(duration, [])
            denominator =  mathtools.greatest_power_of_two_less_equal(
                (duration / node.contents_duration).denominator)
            for x in node:
                if isinstance(x, type(self)):
                    tuplet.extend(recurse(x, durationtools.Duration(x.duration, denominator)))
                else:
                    leaves = x((1, denominator))
                    tuplet.extend(leaves)
                    if 1 < len(leaves):
                        tietools.TieSpanner(leaves)
            if tuplet.multiplier == 1:
                return tuplet[:]
            return [tuplet]
        result = recurse(self, pulse_duration * self.duration)
        tuplettools.remove_trivial_tuplets_in_expr(result)
        return result

    def __contains__(self, expr):
        '''True if expr is in container, otherwise False:

        ::

            >>> container = rhythmtreetools.RhythmTreeContainer()
            >>> a = rhythmtreetools.RhythmTreeLeaf()
            >>> b = rhythmtreetools.RhythmTreeLeaf()
            >>> container.append(a)

        ::

            >>> a in container
            True

        ::

            >>> b in container
            False

        Return boolean.
        '''
        for x in self._children:
            if x is expr:
                return True
        return False
    
    def __deepcopy__(self, memo):
        args = self.__getnewargs__()
        return type(self)(
            args[0],
            [copy.deepcopy(x) for x in args[1]]
            )

    def __delitem__(self, i):
        '''Find node at index or slice `i` in container and detach from parentage:

        ::

            >>> container = rhythmtreetools.RhythmTreeContainer()
            >>> leaf = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> container.append(leaf)
            >>> container.children == (leaf,)
            True
            >>> leaf.parent is container
            True

        ::

            >>> del(container[0])

        ::

            >>> container.children == ()
            True
            >>> leaf.parent is None
            True

        Return `None`.
        '''
        nodes = self[i]
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            node._switch_parent(None)
        self._mark_entire_tree_for_later_update()

    def __eq__(self, other):
        '''True if type, duration and children are equivalent, otherwise False.

        Return boolean.
        '''
        if type(self) == type(other):
            if self.duration == other.duration:
                if self.children == other.children:
                    return True
        return False

    def __getitem__(self, i):
        '''Return node at index `i` in container:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeLeaf()
            >>> c = rhythmtreetools.RhythmTreeContainer()
            >>> d = rhythmtreetools.RhythmTreeLeaf()
            >>> e = rhythmtreetools.RhythmTreeLeaf()
            >>> f = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.extend([b, c, f])
            >>> c.extend([d, e])

        ::

            >>> a[0] is b
            True
            >>> a[1] is c
            True
            >>> a[2] is f
            True

        Return `RhythmTreeNode` instance.    
        '''
        return self._children[i]

    def __getnewargs__(self):
        return (self.duration, self.children)

    def __iter__(self):
        for child in self._children:
            yield child

    def __len__(self):
        '''Return nonnegative integer number of nodes in container.'''
        return len(self._children)

    def __repr__(self):
        result = ['{}('.format(self._class_name)]
        if self.children:
            result.append('\tchildren=(')
            for child in self.children:
                pieces = ['\t\t' + x for x in repr(child).split('\n')]
                result.extend(pieces[:-1])
                result.append(pieces[-1] + ',')
            result.append('\t),')
        result.append('\tduration={}'.format(self.duration))
        result.append('\t)')
        return '\n'.join(result)

    def __setitem__(self, i, expr):
        '''Set `expr` in self at nonnegative integer index `i`, or set `expr` in self at slice i.
        Replace contents of `self[i]` with `expr`.
        Attach parentage to contents of `expr`, and detach parentage of any replaced nodes.

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeLeaf()
            >>> c = rhythmtreetools.RhythmTreeLeaf()

        ::

            >>> a.append(b)
            >>> b.parent is a
            True
            >>> a.children == (b,)
            True

        ::

            >>> a[0] = c

        ::

            >>> c.parent is a
            True
            >>> b.parent is None
            True
            >>> a.children == (c,)
            True

        Return `None`.
        '''
        from abjad.tools.rhythmtreetools.RhythmTreeParser import RhythmTreeParser

        proper_parentage = self.proper_parentage

        if isinstance(i, int):        
            if isinstance(expr, str):
                expr = RhythmTreeParser()(expr)[0]
                assert len(expr) == 1
                expr = expr[0]
            else:
                assert isinstance(expr, self._node_klass)
            old = self[i]
            assert expr not in proper_parentage
            old._switch_parent(None)
            expr._switch_parent(self)
            self._children.insert(i, expr)
        else:
            if isinstance(expr, str):
                expr = RhythmTreeParser()(expr)
            elif isinstance(expr, list) and len(expr) == 1 and isinstance(expr[0], str):
                expr = RhythmTreeParser()(expr[0])
            else:
                assert all([isinstance(x, self._node_klass) for x in expr])
            if i.start == i.stop and i.start is not None \
                and i.stop is not None and i.start <= -len(self):
                start, stop = 0, 0
            else:
                start, stop, stride = i.indices(len(self))
            old = self[start:stop]
            for node in expr:
                assert node not in proper_parentage
            for node in old:
                node._switch_parent(None)
            for node in expr:
                node._switch_parent(self)
            self._children.__setitem__(slice(start, start), expr)
        self._mark_entire_tree_for_later_update()

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _node_klass(self):
        return RhythmTreeNode

    @property
    def _pretty_rtm_format_pieces(self):
        result = []
        result.append('({} ('.format(self.duration))
        for child in self:
            result.extend(['\t' + x for x in child._pretty_rtm_format_pieces])
        result[-1] = result[-1] + '))'
        return result

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def children(self):
        '''The children of a `RhythmTreeContainer` instance:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer()
            >>> b = rhythmtreetools.RhythmTreeContainer()
            >>> c = rhythmtreetools.RhythmTreeLeaf()
            >>> d = rhythmtreetools.RhythmTreeLeaf()
            >>> e = rhythmtreetools.RhythmTreeContainer()

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

        Return tuple of `RhythmTreeNode` instances.
        '''
        return tuple(self._children)

    @property
    def contents_duration(self):
        '''The total duration of the children of a `RhythmTreeContainer` instance:

        ::

            >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

        ::

            >>> tree.contents_duration
            5

        ::

            >>> tree[1].contents_duration
            3

        Return int.
        '''
        return sum([x.duration for x in self])

    @property
    def rtm_format(self):
        '''The node's RTM format:

        ::

            >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
            >>> tree.rtm_format
            '(1 ((1 (1 1)) (1 (1 1))))'

        Return string.
        '''
        return '({} ({}))'.format(
            self.duration,
            ' '.join([x.rtm_format for x in self]))

    ### PUBLIC METHODS ###

    def append(self, node):
        '''Append `node` to container:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer(1)
            >>> b = rhythmtreetools.RhythmTreeLeaf(2)
            >>> c = rhythmtreetools.RhythmTreeLeaf(3)

        ::

            >>> a
            RhythmTreeContainer(
                duration=1
                )

        ::

            >>> a.append(b)
            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                ),
                duration=1
                )

        ::

            >>> a.append(c)
            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                ),
                duration=1
                )

        It is also possible to append with valid RTM strings, so long as they parse
        to a single tree:

        ::

            >>> a.append('(7 (1 1 1))')
            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                    RhythmTreeContainer(
                        children=(
                            RhythmTreeLeaf(
                                duration=1,
                                is_pitched=True,
                                ),
                            RhythmTreeLeaf(
                                duration=1,
                                is_pitched=True,
                                ),
                            RhythmTreeLeaf(
                                duration=1,
                                is_pitched=True,
                                ),
                        ),
                        duration=7
                        ),
                ),
                duration=1
                )

        Return `None`.
        '''
        self.__setitem__(
            slice(len(self), len(self)), 
            [node]
            )

    def extend(self, expr):
        '''Extend `expr` against container:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer(1)
            >>> b = rhythmtreetools.RhythmTreeLeaf(2)
            >>> c = rhythmtreetools.RhythmTreeLeaf(3)

        ::

            >>> a
            RhythmTreeContainer(
                duration=1
                )

        ::

            >>> a.extend([b, c])
            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                ),
                duration=1
                )

        It is also possible to extend with valid RTM strings:

        ::

            >>> a.extend('(4 (1 1)) (5 (1 1))')
            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                    RhythmTreeContainer(
                        children=(
                            RhythmTreeLeaf(
                                duration=1,
                                is_pitched=True,
                                ),
                            RhythmTreeLeaf(
                                duration=1,
                                is_pitched=True,
                                ),
                        ),
                        duration=4
                        ),
                    RhythmTreeContainer(
                        children=(
                            RhythmTreeLeaf(
                                duration=1,
                                is_pitched=True,
                                ),
                            RhythmTreeLeaf(
                                duration=1,
                                is_pitched=True,
                                ),
                        ),
                        duration=5
                        ),
                ),
                duration=1
                )

        Return `None`.
        '''
        self.__setitem__(
            slice(len(self), len(self)),
            #nodes.__getitem__(slice(0, len(nodes)))
            expr
            )

    def index(self, node):
        '''Index `node` in container:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer(1)
            >>> b = rhythmtreetools.RhythmTreeLeaf(2)
            >>> c = rhythmtreetools.RhythmTreeLeaf(3)

        ::

            >>> a.extend([b, c])

        ::

            >>> a.index(b)
            0

        ::

            >>> a.index(c)
            1

        Return nonnegative integer.
        '''
        for i, element in enumerate(self._children):
            if element is node:
                return i
        else:
            raise ValueError('node {!r} not in {!r}.'.format(node, self))

    def insert(self, i, node):
        '''Insert `node` in container at index `i`:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer(1)
            >>> b = rhythmtreetools.RhythmTreeLeaf(2)
            >>> c = rhythmtreetools.RhythmTreeLeaf(3)
            >>> d = rhythmtreetools.RhythmTreeLeaf(100)

        ::

            >>> a.extend([b, c])

        ::

            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                ),
                duration=1
                )

        ::

            >>> a.insert(1, d)

        ::

            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=100,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                ),
                duration=1
                )


        Return `None`.
        '''
        self.__setitem__(
            slice(i, i), 
            [node]
            )

    def pop(self, i=-1):
        '''Pop node at index `i` from container:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer(1)
            >>> b = rhythmtreetools.RhythmTreeLeaf(2)
            >>> c = rhythmtreetools.RhythmTreeLeaf(3)

        ::

            >>> a.extend([b, c])

        ::

            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                ),
                duration=1
                )

        ::

            >>> node = a.pop()

        ::

            >>> node == c
            True

        ::

            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                ),
                duration=1
                )

        Return node.
        '''
        node = self[i]
        del(self[i])
        return node

    def remove(self, node):
        '''Remove `node` from container:

        ::

            >>> a = rhythmtreetools.RhythmTreeContainer(1)
            >>> b = rhythmtreetools.RhythmTreeLeaf(2)
            >>> c = rhythmtreetools.RhythmTreeLeaf(3)

        ::

            >>> a.extend([b, c])

        ::

            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=2,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                ),
                duration=1
                )

        ::

            >>> a.remove(b)

        ::

            >>> a
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=3,
                        is_pitched=True,
                        ),
                ),
                duration=1
                )

        Return `None`.
        '''
        i = self.index(node)
        del(self[i])
