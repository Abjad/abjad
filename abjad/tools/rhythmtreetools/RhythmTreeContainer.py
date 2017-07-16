# -*- coding: utf-8 -*-
from abjad.tools import graphtools
from abjad.tools import durationtools
from abjad.tools import scoretools
from abjad.tools import spannertools
from abjad.tools.datastructuretools.TreeContainer import TreeContainer
from abjad.tools.rhythmtreetools.RhythmTreeMixin import RhythmTreeMixin


class RhythmTreeContainer(RhythmTreeMixin, TreeContainer):
    r'''Rhythm-tree container.

    ::

        >>> import abjad
        >>> from abjad.tools import rhythmtreetools

    ..  container:: example

        Initializes rhythm-tree container:

        ::

            >>> container = rhythmtreetools.RhythmTreeContainer(
            ...     preprolated_duration=1,
            ...     children=[],
            ...     )

        ::

            >>> f(container)
            rhythmtreetools.RhythmTreeContainer(
                preprolated_duration=abjad.Duration(1, 1),
                )

    ..  container:: example

        Similar to Abjad containers, `RhythmTreeContainer` supports a list
        interface, and can be appended, extended, indexed and so forth by other
        `RhythmTreeMixin` subclasses:

        ::

            >>> leaf_a = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=1)
            >>> leaf_b = rhythmtreetools.RhythmTreeLeaf(preprolated_duration=2)
            >>> container.extend([leaf_a, leaf_b])
            >>> f(container)
            rhythmtreetools.RhythmTreeContainer(
                children=(
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=abjad.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=abjad.Duration(2, 1),
                        is_pitched=True,
                        ),
                    ),
                preprolated_duration=abjad.Duration(1, 1),
                )

        ::

            >>> another_container = rhythmtreetools.RhythmTreeContainer(
            ...     preprolated_duration=2)
            >>> another_container.append(
            ...     rhythmtreetools.RhythmTreeLeaf(preprolated_duration=3))
            >>> another_container.append(container[1])
            >>> container.append(another_container)
            >>> f(container)
            rhythmtreetools.RhythmTreeContainer(
                children=(
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=abjad.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeContainer(
                        children=(
                            rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(3, 1),
                                is_pitched=True,
                                ),
                            rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(2, 1),
                                is_pitched=True,
                                ),
                            ),
                        preprolated_duration=abjad.Duration(2, 1),
                        ),
                    ),
                preprolated_duration=abjad.Duration(1, 1),
                )

    ..  container:: example

        Call `RhythmTreeContainer` with a preprolated_duration to generate a
        tuplet structure:

        ::

            >>> components = container((1, 4))
            >>> tuplet = components[0]
            >>> show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> f(tuplet)
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

    _publish_storage_format = True

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

    def __add__(self, argument):
        r'''Concatenate containers self and argument. The operation c = a + b
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

            >>> f(c)
            rhythmtreetools.RhythmTreeContainer(
                children=(
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=abjad.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=abjad.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=abjad.Duration(1, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=abjad.Duration(3, 1),
                        is_pitched=True,
                        ),
                    rhythmtreetools.RhythmTreeLeaf(
                        preprolated_duration=abjad.Duration(4, 1),
                        is_pitched=True,
                        ),
                    ),
                preprolated_duration=abjad.Duration(3, 1),
                )

        Returns new RhythmTreeContainer.
        '''
        from abjad.tools.rhythmtreetools.RhythmTreeParser \
            import RhythmTreeParser
        if isinstance(argument, str):
            argument = RhythmTreeParser()(argument)
            assert 1 == len(argument) and isinstance(argument[0], type(self))
            argument = argument[0]
        container = type(self)(
            preprolated_duration=self.preprolated_duration +
            argument.preprolated_duration)
        container.extend(self[:])
        container.extend(argument[:])
        return container

    def __call__(self, pulse_duration):
        r'''Generates Abjad score components.

        ..  container:: example

            ::

                >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
                >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

            ::

                >>> tree((1, 4))
                [Tuplet(Multiplier(4, 5), "c'16 { 2/3 c'16 c'16 c'16 } c'8")]

            ::

                >>> staff = abjad.Staff(tree((1, 4)))
                >>> show(staff) # doctest: +SKIP

            ..  docs::

                >>> f(staff)
                \new Staff {
                    \times 4/5 {
                        c'16
                        \times 2/3 {
                            c'16
                            c'16
                            c'16
                        }
                        c'8
                    }
                }

        Returns list of components.
        '''
        import abjad
        def recurse(node, tuplet_duration):
            basic_prolated_duration = \
                tuplet_duration / node._get_contents_duration()
            basic_written_duration = \
                basic_prolated_duration.equal_or_greater_power_of_two
            tuplet = abjad.Tuplet(1, [])
            for child in node.children:
                if isinstance(child, type(self)):
                    tuplet.extend(
                        recurse(
                            child,
                            child.preprolated_duration * basic_written_duration
                            )
                        )
                else:
                    leaves = child(basic_written_duration)
                    tuplet.extend(leaves)
                    if 1 < len(leaves):
                        tie = abjad.Tie()
                        abjad.attach(tie, leaves)
            assert tuplet.multiplier == 1, repr(tuplet.multiplier)
            contents_duration = abjad.inspect(tuplet).get_duration()
            target_duration = tuplet_duration
            multiplier = target_duration / contents_duration
            tuplet.multiplier = multiplier
            if tuplet.multiplier == 1:
                return tuplet[:]
            return [tuplet]
        pulse_duration = abjad.Duration(pulse_duration)
        assert 0 < pulse_duration
        result = recurse(self, pulse_duration * self.preprolated_duration)
        for component in result[:]:
            if isinstance(component, abjad.Tuplet):
                if component.is_trivial:
                    component._extract()
        return result

    def __graph__(self, **keywords):
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
        graph = graphtools.GraphvizGraph(
            name='G',
            attributes={
                'bgcolor': 'transparent',
                'truecolor': True,
                },
            )
        node_mapping = {}
        for node in self.nodes:
            graphviz_node = graphtools.GraphvizNode()
            graphviz_node.attributes['label'] = str(node.preprolated_duration)
            if isinstance(node, type(self)):
                graphviz_node.attributes['shape'] = 'triangle'
            else:
                graphviz_node.attributes['shape'] = 'box'
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node.parent is not None:
                graphtools.GraphvizEdge().attach(
                    node_mapping[node.parent],
                    node_mapping[node],
                    )
        return graph

    def __radd__(self, argument):
        r'''Concatenates containers argument and self.

        Returns new RhythmTreeContainer.
        '''
        assert isinstance(argument, type(self))
        return argument.__add__(self)

    def __repr__(self):
        r'''Gets interpreter representation of rhythm tree container.

        Returns string.
        '''
        return '{}(({}, {}))'.format(
            type(self).__name__,
            self.duration.numerator,
            self.duration.denominator,
            )

    def __setitem__(self, i, argument):
        r'''Set `argument` in self at nonnegative integer index `i`,
        or set `argument` in self at slice i.
        Replace contents of `self[i]` with `argument`.
        Attach parentage to contents of `argument`,
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
            if isinstance(argument, str):
                argument = RhythmTreeParser()(argument)[0]
                assert len(argument) == 1
                argument = argument[0]
            else:
                assert isinstance(argument, self._node_class)
            old = self[i]
            assert argument not in proper_parentage
            old._set_parent(None)
            argument._set_parent(self)
            self._children.insert(i, argument)
        else:
            if isinstance(argument, str):
                argument = RhythmTreeParser()(argument)
            elif isinstance(argument, list) and len(argument) == 1 and \
                isinstance(argument[0], str):
                argument = RhythmTreeParser()(argument[0])
            else:
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

    ### PRIVATE PROPERTIES ###

    def _get_contents_duration(self):
        r'''The total preprolated_duration of the children
        of a `RhythmTreeContainer` instance:

        ::

            >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = rhythmtreetools.RhythmTreeParser()(rtm)[0]

        ::

            >>> tree._get_contents_duration()
            Duration(5, 1)

        ::

            >>> tree[1]._get_contents_duration()
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
