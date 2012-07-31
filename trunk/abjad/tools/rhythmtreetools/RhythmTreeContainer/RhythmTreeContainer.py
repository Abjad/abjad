from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import tuplettools
from abjad.tools.rhythmtreetools.RhythmTreeNode import RhythmTreeNode
import copy


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
                    pitched=True,
                    ),
                RhythmTreeLeaf(
                    duration=2,
                    pitched=True,
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
                    pitched=True,
                    ),
                RhythmTreeContainer(
                    children=(
                        RhythmTreeLeaf(
                            duration=3,
                            pitched=True,
                            ),
                        RhythmTreeLeaf(
                            duration=2,
                            pitched=True,
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
        FixedDurationTuplet(1/4, [c'8, {@ 5:4 c'8., c'8 @}])
        >>> f(_)
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

    __slots__ = ('_children', '_duration', '_offsets', '_offsets_are_current', '_parent')

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

    def __call__(self, pulse_duration):
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
                    tuplet.extend(x((1, denominator)))
            if tuplet.multiplier == 1:
                return tuplet[:]
            return [tuplet]
        result = recurse(self, pulse_duration * self.duration)
        tuplettools.remove_trivial_tuplets_in_expr(result)
        return result

    def __contains__(self, node):
        for x in self._children:
            if x is node:
                return True
        return False
    
    def __deepcopy__(self, memo):
        args = self.__getnewargs__()
        return type(self)(
            args[0],
            [copy.deepcopy(x) for x in args[1]]
            )

    def __delitem__(self, i):
        nodes = self[i]
        if not isinstance(nodes, list):
            nodes = [nodes]
        for node in nodes:
            node._switch_parent(None)
        self._mark_entire_tree_for_later_update()

    def __eq__(self, other):
        if type(self) == type(other):
            if self.duration == other.duration:
                if self.children == other.children:
                    return True
        return False

    def __getitem__(self, i):
        return self._children[i]

    def __getnewargs__(self):
        return (self.duration, self.children)

    def __iter__(self):
        for child in self._children:
            yield child

    def __len__(self):
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
        from abjad.tools.rhythmtreetools.RhythmTreeParser import RhythmTreeParser

        if isinstance(i, int):        
            if isinstance(expr, str):
                expr = RhythmTreeParser()(expr)[0]
                assert len(expr) == 1
                expr = expr[0]
            else:
                assert isinstance(expr, self.node_klass)
            old = self[i]
            old._switch_parent(None)
            expr._switch_parent(self)
            self._children.insert(i, expr)
        else:
            if isinstance(expr, str):
                expr = RhythmTreeParser()(expr)
            elif isinstance(expr, list) and len(expr) == 1 and isinstance(expr[0], str):
                expr = RhythmTreeParser()(expr[0])
            else:
                assert all([isinstance(x, self.node_klass) for x in expr])
            if i.start == i.stop and i.start is not None \
                and i.stop is not None and i.start <= -len(self):
                start, stop = 0, 0
            else:
                start, stop, stride = i.indices(len(self))
            old = self[start:stop]
            for node in old:
                node._switch_parent(None)
            for node in expr:
                node._switch_parent(self)
            self._children.__setitem__(slice(start, start), expr)
        self._mark_entire_tree_for_later_update()

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def children(self):
        return tuple(self._children)

    @property
    def contents_duration(self):
        return sum([x.duration for x in self])

    @property
    def node_klass(self):
        return RhythmTreeNode

    @property
    def rtm_format(self):
        return '({} ({}))'.format(
            self.duration,
            ' '.join([x.rtm_format for x in self]))

    ### PUBLIC METHODS ###

    def append(self, node):
        self.__setitem__(
            slice(len(self), len(self)), 
            [node]
            )

    def extend(self, nodes):
        self.__setitem__(
            slice(len(self), len(self)),
            nodes.__getitem__(slice(0, len(nodes)))
            )

    def index(self, node):
        for i, element in enumerate(self._children):
            if element is node:
                return i
        else:
            raise ValueError('node {!r} not in {!r}.'.format(node, self))

    def insert(self, i, node):
        self.__setitem__(
            slice(i, i), 
            [node]
            )

    def pop(self, i=-1):
        node = self[i]
        del(self[i])
        return node

    def remove(self, node):
        i = self.index(node)
        del(self[i])
