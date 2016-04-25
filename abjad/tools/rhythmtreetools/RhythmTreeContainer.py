# -*- coding: utf-8 -*-
from abjad.tools import documentationtools
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.datastructuretools.TreeContainer import TreeContainer
from abjad.tools.rhythmtreetools.RhythmTreeMixin import RhythmTreeMixin


class RhythmTreeContainer(RhythmTreeMixin, TreeContainer):
    r'''A rhythm-tree container.

    ..  container:: example

        **Example 1.** Initializes a rhythm-tree container:

        ::

            >>> container = rhythmtreetools.RhythmTreeContainer(
            ...     preprolated_duration=1, children=[])
            >>> print(format(container))
            rhythmtreetools.RhythmTreeContainer(
                preprolated_duration=durationtools.Duration(1, 1),
                )

    ..  container:: example

        **Example 2.** Similar to Abjad containers, `RhythmTreeContainer`
        supports a list interface, and can be appended, extended, indexed and
        so forth by other `RhythmTreeMixin` subclasses:

        ::

            >>> leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
            >>> leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
            >>> container.extend([leaf_a, leaf_b])
            >>> print(format(container))
            rhythmtreetools.RhythmTreeContainer(
                children=(
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=durationtools.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=durationtools.Duration(2, 1),
                        is_pitched=True,
                        ),
                    ),
                preprolated_duration=durationtools.Duration(1, 1),
                )

        ::

            >>> another_container = rhythmtreetools.RhythmTreeContainer(
            ...     preprolated_duration=2)
            >>> another_container.append(
            ...     rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3))
            >>> another_container.append(container[1])
            >>> container.append(another_container)
            >>> print(format(container))
            rhythmtreetools.RhythmTreeContainer(
                children=(
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=durationtools.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeContainer(
                        children=(
                            rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=durationtools.Duration(3, 1),
                                is_pitched=True,
                                ),
                            rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=durationtools.Duration(2, 1),
                                is_pitched=True,
                                ),
                            ),
                        preprolated_duration=durationtools.Duration(2, 1),
                        ),
                    ),
                preprolated_duration=durationtools.Duration(1, 1),
                )

    ..  container:: example

        **Example 3.** Call `RhythmTreeContainer` with a preprolated_duration
        to generate a tuplet structure:

        ::

            >>> list_ = container((1, 4))
            >>> list_
            [FixedDurationTuplet(Duration(1, 4), "c'8 { 4/5 c'8. c'8 }")]
            >>> tuplet = list_[0]
            >>> show(tuplet) # doctest: +SKIP

        ..  doctest::

            >>> print(format(_[0]))
            \times 2/3 {
                c'8
                \times 4/5 {
                    c'8.
                    c'8
                }
            }

    Returns `RhythmTreeContainer` instance.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_duration',
        '_offset',
        '_offsets_are_current',
        )

    ### INITIALIZER ###

    def __init__(self, children=None, preprolated_duration=1, name=None):
        TreeContainer.__init__(self, name=name)
        RhythmTreeMixin.__init__(self, preprolated_duration=preprolated_duration)
        if isinstance(children, (list, str, tuple)):
            self.extend(children)
        elif children is not None:
            message = 'can not instantiate {} with {!r}.'
            raise ValueError(message.format(type(self), children))

    ### SPECIAL METHODS ###

    def __add__(self, expr):
        r'''Concatenate containers self and expr. The operation c = a + b
        returns a new RhythmTreeContainer c with the content of both a and b,
        and a preprolated_duration equal to the sum of the durations
        of a and b. The operation is non-commutative: the content of the
        first operand will be placed before the content of the second operand:

        ::

            >>> a = rhythmtreetools.RhythmTreeParser()('(1 (1 1 1))')[0]
            >>> b = rhythmtreetools.RhythmTreeParser()('(2 (3 4))')[0]

        ::

            >>> c = a + b

        ::

            >>> c.preprolated_duration
            Duration(3, 1)

        ::

            >>> print(format(c))
            rhythmtreetools.RhythmTreeContainer(
                children=(
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=durationtools.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=durationtools.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=durationtools.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=durationtools.Duration(3, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=durationtools.Duration(4, 1),
                        is_pitched=True,
                        ),
                    ),
                preprolated_duration=durationtools.Duration(3, 1),
                )

        Returns new RhythmTreeContainer.
        '''
        from abjad.tools.rhythmtreetools.RhythmTreeParser \
            import RhythmTreeParser
        if isinstance(expr, str):
            expr = RhythmTreeParser()(expr)
            assert 1 == len(expr) and isinstance(expr[0], type(self))
            expr = expr[0]
        container = type(self)(
            preprolated_duration=self.preprolated_duration +
            expr.preprolated_duration)
        container.extend(self[:])
        container.extend(expr[:])
        return container

    def __call__(self, pulse_duration):
        r'''Generate Abjad score components:

        ::

            >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

        ::

            >>> tree((1, 4))
            [FixedDurationTuplet(Duration(1, 4), "c'16 { 2/3 c'16 c'16 c'16 } c'8")]

        Returns sequence of components.
        '''
        def recurse(node, tuplet_duration):
            basic_prolated_duration = tuplet_duration / node._contents_duration
            basic_written_duration = \
                basic_prolated_duration.equal_or_greater_power_of_two
            tuplet = scoretools.FixedDurationTuplet(tuplet_duration, [])
            for child in node.children:
                if isinstance(child, type(self)):
                    tuplet.extend(recurse(
                        child,
                        child.preprolated_duration * basic_written_duration))
                else:
                    leaves = child(basic_written_duration)
                    tuplet.extend(leaves)
                    if 1 < len(leaves):
                        tie = spannertools.Tie()
                        attach(tie, leaves)
            if tuplet.multiplier == 1:
                return tuplet[:]
            return [tuplet]
        from abjad.tools.topleveltools import attach
        pulse_duration = durationtools.Duration(pulse_duration)
        assert 0 < pulse_duration
        result = recurse(self, pulse_duration * self.preprolated_duration)
        for component in result[:]:
            if isinstance(component, scoretools.Tuplet):
                if component.is_trivial:
                    component._extract()
        return result

    def __graph__(self, **kwargs):
        r'''The GraphvizGraph representation of the RhythmTreeContainer:

        ::

            >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
            >>> graph = tree.__graph__()
            >>> print(str(graph))
            digraph G {
                graph [bgcolor=transparent,
                    truecolor=true];
                node_0 [label="1",
                    shape=triangle];
                node_1 [label="1",
                    shape=box];
                node_2 [label="2",
                    shape=triangle];
                node_3 [label="1",
                    shape=box];
                node_4 [label="1",
                    shape=box];
                node_5 [label="1",
                    shape=box];
                node_6 [label="2",
                    shape=box];
                node_0 -> node_1;
                node_0 -> node_2;
                node_0 -> node_6;
                node_2 -> node_3;
                node_2 -> node_4;
                node_2 -> node_5;
            }

        ::

            >>> topleveltools.graph(graph) # doctest: +SKIP

        Return `GraphvizGraph` instance.
        '''
        graph = documentationtools.GraphvizGraph(
            name='G',
            attributes={
                'bgcolor': 'transparent',
                'truecolor': True,
                },
            )
        node_mapping = {}
        for node in self.nodes:
            graphviz_node = documentationtools.GraphvizNode()
            graphviz_node.attributes['label'] = str(node.preprolated_duration)
            if isinstance(node, type(self)):
                graphviz_node.attributes['shape'] = 'triangle'
            else:
                graphviz_node.attributes['shape'] = 'box'
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node.parent is not None:
                documentationtools.GraphvizEdge().attach(
                    node_mapping[node.parent],
                    node_mapping[node],
                    )
        return graph

    def __repr__(self):
        r'''Gets interpreter representation of rhythm tree container.

        Returns string.
        '''
        return '{}(({}, {}))'.format(
            type(self).__name__,
            self.duration.numerator,
            self.duration.denominator,
            )

    def __setitem__(self, i, expr):
        r'''Set `expr` in self at nonnegative integer index `i`,
        or set `expr` in self at slice i.
        Replace contents of `self[i]` with `expr`.
        Attach parentage to contents of `expr`,
        and detach parentage of any replaced nodes.

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
        from abjad.tools.rhythmtreetools.RhythmTreeParser \
            import RhythmTreeParser

        proper_parentage = self.proper_parentage

        if isinstance(i, int):
            if isinstance(expr, str):
                expr = RhythmTreeParser()(expr)[0]
                assert len(expr) == 1
                expr = expr[0]
            else:
                assert isinstance(expr, self._node_class)
            old = self[i]
            assert expr not in proper_parentage
            old._set_parent(None)
            expr._set_parent(self)
            self._children.insert(i, expr)
        else:
            if isinstance(expr, str):
                expr = RhythmTreeParser()(expr)
            elif isinstance(expr, list) and len(expr) == 1 and \
                isinstance(expr[0], str):
                expr = RhythmTreeParser()(expr[0])
            else:
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

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_duration(self):
        r'''The total preprolated_duration of the children
        of a `RhythmTreeContainer` instance:

        ::

            >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

        ::

            >>> tree._contents_duration
            Duration(5, 1)

        ::

            >>> tree[1]._contents_duration
            Duration(3, 1)

        Returns int.
        '''
        return sum([x.preprolated_duration for x in self])

    @property
    def _leaf_class(self):
        from abjad.tools import rhythmtreetools
        return rhythmtreetools.RhythmTreeLeaf

    @property
    def _node_class(self):
        return RhythmTreeMixin

    @property
    def _pretty_rtm_format_pieces(self):
        result = []
        result.append('({!s} ('.format(self.preprolated_duration))
        for child in self:
            result.extend(['    ' + x for x in child._pretty_rtm_format_pieces])
        result[-1] = result[-1] + '))'
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def rtm_format(self):
        r'''The node's RTM format:

        ::

            >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]
            >>> tree.rtm_format
            '(1 ((1 (1 1)) (1 (1 1))))'

        Returns string.
        '''
        return '({!s} ({}))'.format(
            self.preprolated_duration,
            ' '.join([x.rtm_format for x in self]))
