from abjad.tools import documentationtools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import tietools
from abjad.tools import tuplettools
from abjad.tools.datastructuretools.TreeContainer import TreeContainer
from abjad.tools.rhythmtreetools.RhythmTreeNode import RhythmTreeNode


class RhythmTreeContainer(RhythmTreeNode, TreeContainer):
    r'''A container node in a rhythm tree structure:

    ::

        >>> container = rhythmtreetools.RhythmTreeContainer(duration=1, children=[])
        >>> container
        RhythmTreeContainer(
            duration=Duration(1, 1)
            )

    Similar to Abjad containers, `RhythmTreeContainer` supports a list interface,
    and can be appended, extended, indexed and so forth by other `RhythmTreeNode`
    subclasses:

    ::

        >>> leaf_a = rhythmtreetools.RhythmTreeLeaf(duration=1)
        >>> leaf_b = rhythmtreetools.RhythmTreeLeaf(duration=2)
        >>> container.extend([leaf_a, leaf_b])
        >>> container
        RhythmTreeContainer(
            children=(
                RhythmTreeLeaf(
                    duration=Duration(1, 1),
                    is_pitched=True
                    ),
                RhythmTreeLeaf(
                    duration=Duration(2, 1),
                    is_pitched=True
                    )
                ),
            duration=Duration(1, 1)
            )

    ::

        >>> another_container = rhythmtreetools.RhythmTreeContainer(duration=2)
        >>> another_container.append(rhythmtreetools.RhythmTreeLeaf(duration=3))
        >>> another_container.append(container[1])
        >>> container.append(another_container)
        >>> container
        RhythmTreeContainer(
            children=(
                RhythmTreeLeaf(
                    duration=Duration(1, 1),
                    is_pitched=True
                    ),
                RhythmTreeContainer(
                    children=(
                        RhythmTreeLeaf(
                            duration=Duration(3, 1),
                            is_pitched=True
                            ),
                        RhythmTreeLeaf(
                            duration=Duration(2, 1),
                            is_pitched=True
                            )
                        ),
                    duration=Duration(2, 1)
                    )
                ),
            duration=Duration(1, 1)
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

    ### INITIALIZER ###

    def __init__(self, children=None, duration=1, name=None):
        RhythmTreeNode.__init__(self, duration=duration, name=name)
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
            Duration(3, 1)

        ::

            >>> c
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=Duration(1, 1),
                        is_pitched=True
                        ),
                    RhythmTreeLeaf(
                        duration=Duration(1, 1),
                        is_pitched=True
                        ),
                    RhythmTreeLeaf(
                        duration=Duration(1, 1),
                        is_pitched=True
                        ),
                    RhythmTreeLeaf(
                        duration=Duration(3, 1),
                        is_pitched=True
                        ),
                    RhythmTreeLeaf(
                        duration=Duration(4, 1),
                        is_pitched=True
                        )
                    ),
                duration=Duration(3, 1)
                )

        Return new RhythmTreeContainer.
        '''
        from abjad.tools.rhythmtreetools.RhythmTreeParser import RhythmTreeParser
        if isinstance(expr, str):
            expr = RhythmTreeParser()(expr)
            assert 1 == len(expr) and isinstance(expr[0], type(self))
            expr = expr[0]
        container = type(self)(duration=self.duration + expr.duration)
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
        def recurse(node, tuplet_duration):
            basic_prolated_duration = tuplet_duration / node.contents_duration
            basic_written_duration = basic_prolated_duration.equal_or_greater_power_of_two
            tuplet = tuplettools.FixedDurationTuplet(tuplet_duration, [])
            for child in node.children:
                if isinstance(child, type(self)):
                    tuplet.extend(recurse(child, child.duration * basic_written_duration))
                else:
                    leaves = child(basic_written_duration)
                    tuplet.extend(leaves)
                    if 1 < len(leaves):
                        tietools.TieSpanner(leaves)
            if tuplet.multiplier == 1:
                return tuplet[:]
            return [tuplet]
        result = recurse(self, pulse_duration * self.duration)
        tuplettools.remove_trivial_tuplets_in_expr(result)
        return result

    def __eq__(self, other):
        '''True if type, duration and children are equivalent, otherwise False.

        Return boolean.
        '''
        if type(self) == type(other):
            if self.duration == other.duration:
                if self.children == other.children:
                    return True
        return False

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
    def _leaf_klass(self):
        from abjad.tools import rhythmtreetools
        return rhythmtreetools.RhythmTreeLeaf

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
    def contents_duration(self):
        '''The total duration of the children of a `RhythmTreeContainer` instance:

        ::

            >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

        ::

            >>> tree.contents_duration
            Duration(5, 1)

        ::

            >>> tree[1].contents_duration
            Duration(3, 1)

        Return int.
        '''
        return sum([x.duration for x in self])

    @property
    def graphviz_graph(self):
        graph = documentationtools.GraphvizGraph(name='G')
        node_mapping = {}
        for node in self.nodes:
            graphviz_node = documentationtools.GraphvizNode()
            graphviz_node.attributes['label'] = str(node.duration)
            if isinstance(node, type(self)):
                graphviz_node.attributes['shape'] = 'triangle'   
            else:
                graphviz_node.attributes['shape'] = 'box'
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node.parent is not None:
                documentationtools.GraphvizEdge()(
                    node_mapping[node.parent],
                    node_mapping[node],
                    )
        return graph

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


