"""
Tools for modeling "rhythm-trees".
"""

import abc
import typing
import uqbar.containers
import uqbar.graphs
from abjad import Fraction
from abjad import core
from abjad import mathtools
from abjad import system
from abjad.system import Parser


class RhythmTreeMixin(system.AbjadObject):
    """
    Abstract rhythm-tree node.
    """

    ### CLASS VARIABLES ###

    _state_flag_names: typing.Tuple[str, ...] = ('_offsets_are_current',)

    ### INITIALIZER ###

    @abc.abstractmethod
    def __init__(self, preprolated_duration=1):
        import abjad
        self._duration = 0
        self._offset = abjad.Offset(0)
        self._offsets_are_current = False
        self.preprolated_duration = preprolated_duration

    ### SPECIAL METHODS ###

    @abc.abstractmethod
    def __call__(self, pulse_duration):
        """
        Calls rhythm tree node on ``pulse_duration``.
        """
        raise NotImplementedError

    ### PRIVATE METHODS ###

    def _update_offsets_of_entire_tree(self):
        def recurse(container, current_offset):
            container._offset = current_offset
            container._offsets_are_current = True
            for child in container:
                if getattr(child, 'children', None) is not None:
                    current_offset = recurse(child, current_offset)
                else:
                    child._offset = current_offset
                    child._offsets_are_current = True
                    current_offset += child.duration
            return current_offset
        import abjad
        offset = abjad.Offset(0)
        root = self.root
        if root is None:
            root = self
        if root is self and not hasattr(self, 'children'):
            self._offset = offset
            self._offsets_are_current = True
        else:
            recurse(root, offset)

    def _update_offsets_of_entire_tree_if_necessary(self):
        if not self._get_node_state_flags()['_offsets_are_current']:
            self._update_offsets_of_entire_tree()

    ### PRIVATE PROPERTIES ###

    @abc.abstractproperty
    def _pretty_rtm_format_pieces(self):
        raise NotImplementedError

    @property
    def _depthwise_inventory(self):
        def recurse(node):
            if node.depth not in inventory:
                inventory[node.depth] = []
            inventory[node.depth].append(node)
            if getattr(node, 'children', None) is not None:
                for child in node.children:
                    recurse(child)
        inventory = {}
        recurse(self)
        return inventory

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        """
        The preprolated_duration of the node:

        >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
        >>> tree = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]

        >>> tree.duration
        Duration(1, 1)

        >>> tree[1].duration
        Duration(1, 2)

        >>> tree[1][1].duration
        Duration(1, 4)

        Return ``Duration`` instance.
        """
        return self.prolation * self.preprolated_duration

    @property
    def parentage_ratios(self):
        """
        A sequence describing the relative durations of the nodes in a
        node's improper parentage.

        The first item in the sequence is the preprolated_duration of
        the root node, and subsequent items are pairs of the
        preprolated duration of the next node in the parentage and
        the total preprolated_duration of that node and its siblings:


        >>> a = abjad.rhythmtrees.RhythmTreeContainer(preprolated_duration=1)
        >>> b = abjad.rhythmtrees.RhythmTreeContainer(preprolated_duration=2)
        >>> c = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3)
        >>> d = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=4)
        >>> e = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=5)

        >>> a.extend([b, c])
        >>> b.extend([d, e])

        >>> a.parentage_ratios
        (Duration(1, 1),)

        >>> b.parentage_ratios
        (Duration(1, 1), (Duration(2, 1), Duration(5, 1)))

        >>> c.parentage_ratios
        (Duration(1, 1), (Duration(3, 1), Duration(5, 1)))

        >>> d.parentage_ratios
        (Duration(1, 1), (Duration(2, 1), Duration(5, 1)), (Duration(4, 1), Duration(9, 1)))

        >>> e.parentage_ratios
        (Duration(1, 1), (Duration(2, 1), Duration(5, 1)), (Duration(5, 1), Duration(9, 1)))

        Returns tuple.
        """
        result = []
        node = self
        while node.parent is not None:
            result.append((
                node.preprolated_duration,
                node.parent._get_contents_duration(),
            ))
            node = node.parent
        result.append(node.preprolated_duration)
        return tuple(reversed(result))

    @property
    def preprolated_duration(self):
        """
        The node's preprolated_duration in pulses:

        >>> node = abjad.rhythmtrees.RhythmTreeLeaf(
        ...     preprolated_duration=1)
        >>> node.preprolated_duration
        Duration(1, 1)

        >>> node.preprolated_duration = 2
        >>> node.preprolated_duration
        Duration(2, 1)

        Returns int.
        """
        return self._duration

    @preprolated_duration.setter
    def preprolated_duration(self, argument):
        import abjad
        if not isinstance(argument, Fraction):
            argument = abjad.Duration(argument)
        assert 0 < argument
        self._duration = argument
        self._mark_entire_tree_for_later_update()

    @property
    def pretty_rtm_format(self):
        """
        The node's pretty-printed RTM format:

        >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
        >>> tree = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]
        >>> print(tree.pretty_rtm_format)
        (1 (
            (1 (
                1
                1))
            (1 (
                1
                1))))

        Returns string.
        """
        return '\n'.join(self._pretty_rtm_format_pieces)

    @property
    def prolation(self):
        """
        Prolation of rhythm tree node.

        Returns multiplier.
        """
        return mathtools.cumulative_products(self.prolations)[-1]

    @property
    def prolations(self):
        """
        Prolations of rhythm tree node.

        Returns tuple.
        """
        import abjad
        prolations = [abjad.Multiplier(1)]
        pairs = abjad.sequence(self.parentage).nwise()
        for child, parent in pairs:
            prolations.append(abjad.Multiplier(
                parent.preprolated_duration, parent._get_contents_duration()))
        return tuple(prolations)

    @abc.abstractproperty
    def rtm_format(self):
        """
        The node's RTM format:

        >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
        >>> tree = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]
        >>> tree.rtm_format
        '(1 ((1 (1 1)) (1 (1 1))))'

        Returns string.
        """
        raise NotImplementedError

    @property
    def start_offset(self):
        """
        The starting offset of a node in a rhythm-tree relative the root.

        >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
        >>> tree = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]

        >>> tree.start_offset
        Offset(0, 1)

        >>> tree[1].start_offset
        Offset(1, 2)

        >>> tree[0][1].start_offset
        Offset(1, 4)

        Returns Offset instance.
        """
        self._update_offsets_of_entire_tree_if_necessary()
        return self._offset

    @property
    def stop_offset(self):
        """
        The stopping offset of a node in a rhythm-tree relative the root.
        """
        return self.start_offset + self.duration


class RhythmTreeLeaf(RhythmTreeMixin, uqbar.containers.UniqueTreeNode):
    """
    Rhythm-tree leaf.

    ..  container:: example

        >>> leaf = abjad.rhythmtrees.RhythmTreeLeaf(
        ...     preprolated_duration=5, is_pitched=True)
        >>> leaf
        RhythmTreeLeaf(preprolated_duration=Duration(5, 1), is_pitched=True)

    ..  container:: example

        Calls with a pulse preprolated duration to generate leaves:

        >>> result = leaf((1, 8))
        >>> result
        Selection([Note("c'2"), Note("c'8")])

    ..  container:: example

        Generates rests when called if ``is_pitched`` is false:

        >>> abjad.rhythmtrees.RhythmTreeLeaf(
        ...     preprolated_duration=7, is_pitched=False)((1, 16))
        Selection([Rest('r4..')])

    """

    ### INITIALIZER ###

    def __init__(
        self,
        preprolated_duration=1,
        is_pitched=True,
        name=None,
    ):
        uqbar.containers.UniqueTreeNode.__init__(self, name=name)
        RhythmTreeMixin.__init__(self, preprolated_duration=preprolated_duration)
        self.is_pitched = is_pitched

    ### SPECIAL METHODS ###

    def __call__(self, pulse_duration):
        """
        Generate Abjad score components:

        >>> leaf = abjad.rhythmtrees.RhythmTreeLeaf(5)
        >>> leaf((1, 4))
        Selection([Note("c'1"), Note("c'4")])

        Returns sequence of components.
        """
        import abjad
        pulse_duration = abjad.Duration(pulse_duration)
        total_duration = pulse_duration * self.preprolated_duration
        maker = abjad.LeafMaker()
        if self.is_pitched:
            return maker(0, total_duration)
        return maker([None], total_duration)

    def __graph__(self, **keywords):
        """
        Graphviz graph of rhythm tree leaf.
        """
        graph = uqbar.graphs.Graph(name='G')
        node = uqbar.graphs.Node(
            attributes={
                'label': str(self.preprolated_duration),
                'shape': 'box'
                }
            )
        graph.append(node)
        return graph

    ### PRIVATE PROPERTIES ###

    @property
    def _pretty_rtm_format_pieces(self):
        return [str(self.preprolated_duration)]

    ### PUBLIC PROPERTIES ###

    @property
    def rtm_format(self):
        """
        RTM format of rhythm tree leaf.

        >>> abjad.rhythmtrees.RhythmTreeLeaf(1, is_pitched=True).rtm_format
        '1'
        >>> abjad.rhythmtrees.RhythmTreeLeaf(5, is_pitched=False).rtm_format
        '-5'

        Returns string.
        """
        if self.is_pitched:
            return '{!s}'.format(self.preprolated_duration)
        return '-{!s}'.format(self.preprolated_duration)

    ### PUBLIC PROPERTIES ###

    @property
    def is_pitched(self):
        """
        Gets and sets boolean equal to  true if leaf is pitched.

        >>> leaf = abjad.rhythmtrees.RhythmTreeLeaf()
        >>> leaf.is_pitched
        True

        >>> leaf.is_pitched = False
        >>> leaf.is_pitched
        False

        Returns true or false.
        """
        return self._is_pitched

    @is_pitched.setter
    def is_pitched(self, argument):
        self._is_pitched = bool(argument)


class RhythmTreeContainer(RhythmTreeMixin, uqbar.containers.UniqueTreeContainer):
    r"""
    Rhythm-tree container.

    ..  container:: example

        Initializes rhythm-tree container:

        >>> container = abjad.rhythmtrees.RhythmTreeContainer(
        ...     preprolated_duration=1,
        ...     children=[],
        ...     )

        >>> abjad.f(container)
        abjad.rhythmtrees.RhythmTreeContainer(
            children=(),
            preprolated_duration=abjad.Duration(1, 1),
            )

    ..  container:: example

        Similar to Abjad containers, ``RhythmTreeContainer`` supports a list
        interface, and can be appended, extended, indexed and so forth by other
        ``RhythmTreeMixin`` subclasses:

        >>> leaf_a = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=1)
        >>> leaf_b = abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=2)
        >>> container.extend([leaf_a, leaf_b])
        >>> abjad.f(container)
        abjad.rhythmtrees.RhythmTreeContainer(
            children=(
                abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    is_pitched=True,
                    ),
                abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=abjad.Duration(2, 1),
                    is_pitched=True,
                    ),
                ),
            preprolated_duration=abjad.Duration(1, 1),
            )

        >>> another_container = abjad.rhythmtrees.RhythmTreeContainer(
        ...     preprolated_duration=2)
        >>> another_container.append(
        ...     abjad.rhythmtrees.RhythmTreeLeaf(preprolated_duration=3))
        >>> another_container.append(container[1])
        >>> container.append(another_container)
        >>> abjad.f(container)
        abjad.rhythmtrees.RhythmTreeContainer(
            children=(
                abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    is_pitched=True,
                    ),
                abjad.rhythmtrees.RhythmTreeContainer(
                    children=(
                        abjad.rhythmtrees.RhythmTreeLeaf(
                            preprolated_duration=abjad.Duration(3, 1),
                            is_pitched=True,
                            ),
                        abjad.rhythmtrees.RhythmTreeLeaf(
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

        Call ``RhythmTreeContainer`` with a preprolated_duration to generate a
        tuplet structure:

        >>> components = container((1, 4))
        >>> tuplet = components[0]
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \times 2/3 {
                c'8
                \times 4/5 {
                    c'8.
                    c'8
                }
            }

    Returns ``RhythmTreeContainer`` instance.
    """

    ### CLASS VARIABLES ###

    _publish_storage_format = True

    ### INITIALIZER ###

    def __init__(self, children=None, preprolated_duration=1, name=None):
        uqbar.containers.UniqueTreeContainer.__init__(self, name=name)
        RhythmTreeMixin.__init__(self, preprolated_duration=preprolated_duration)
        if isinstance(children, (list, str, tuple)):
            self.extend(children)
        elif children is not None:
            message = 'can not instantiate {} with {!r}.'
            raise ValueError(message.format(type(self), children))

    ### SPECIAL METHODS ###

    def __add__(self, argument):
        r"""
        Concatenate containers self and argument. The operation c = a + b
        returns a new RhythmTreeContainer c with the content of both a and b,
        and a preprolated_duration equal to the sum of the durations
        of a and b. The operation is non-commutative: the content of the
        first operand will be placed before the content of the second operand:

        >>> a = abjad.rhythmtrees.RhythmTreeParser()('(1 (1 1 1))')[0]
        >>> b = abjad.rhythmtrees.RhythmTreeParser()('(2 (3 4))')[0]

        >>> c = a + b

        >>> c.preprolated_duration
        Duration(3, 1)

        >>> abjad.f(c)
        abjad.rhythmtrees.RhythmTreeContainer(
            children=(
                abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    is_pitched=True,
                    ),
                abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    is_pitched=True,
                    ),
                abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    is_pitched=True,
                    ),
                abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=abjad.Duration(3, 1),
                    is_pitched=True,
                    ),
                abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=abjad.Duration(4, 1),
                    is_pitched=True,
                    ),
                ),
            preprolated_duration=abjad.Duration(3, 1),
            )

        Returns new RhythmTreeContainer.
        """
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
        r"""
        Generates Abjad score components.

        ..  container:: example

            >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
            >>> tree = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]

            >>> tree((1, 4))
            [Tuplet(Multiplier(4, 5), "c'16 { 2/3 c'16 c'16 c'16 } c'8")]

            >>> staff = abjad.Staff(tree((1, 4)))
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
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
        """
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
            contents_duration = abjad.inspect(tuplet).duration()
            target_duration = tuplet_duration
            multiplier = target_duration / contents_duration
            tuplet.multiplier = multiplier
            if tuplet.multiplier == 1:
                return tuplet[:]
            return [tuplet]
        import abjad
        pulse_duration = abjad.Duration(pulse_duration)
        assert 0 < pulse_duration
        result = recurse(self, pulse_duration * self.preprolated_duration)
        for component in result[:]:
            if isinstance(component, abjad.Tuplet):
                if component.trivial():
                    component._extract()
        return result

    def __graph__(self, **keywords):
        r"""
        The Graph representation of the RhythmTreeContainer:

        >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
        >>> tree = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]
        >>> graph = tree.__graph__()
        >>> print(format(graph, 'graphviz'))
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

        >>> abjad.graph(graph) # doctest: +SKIP

        Return ``Graph`` instance.
        """
        graph = uqbar.graphs.Graph(
            name='G',
            attributes={
                'bgcolor': 'transparent',
                'truecolor': True,
                },
            )
        node_mapping = {}
        nodes = [self]
        nodes.extend(self.depth_first())
        for node in nodes:
            graphviz_node = uqbar.graphs.Node()
            graphviz_node.attributes['label'] = str(node.preprolated_duration)
            if isinstance(node, type(self)):
                graphviz_node.attributes['shape'] = 'triangle'
            else:
                graphviz_node.attributes['shape'] = 'box'
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node.parent is not None:
                uqbar.graphs.Edge().attach(
                    node_mapping[node.parent],
                    node_mapping[node],
                    )
        return graph

    def __radd__(self, argument):
        """
        Concatenates containers argument and self.

        Returns new RhythmTreeContainer.
        """
        assert isinstance(argument, type(self))
        return argument.__add__(self)

    def __repr__(self):
        """
        Gets interpreter representation of rhythm tree container.

        Returns string.
        """
        return '{}(({}, {}))'.format(
            type(self).__name__,
            self.duration.numerator,
            self.duration.denominator,
            )

    ### PRIVATE METHODS ###

    def _prepare_setitem_single(self, expr):
        if isinstance(expr, str):
            expr = RhythmTreeParser()(expr)[0]
            assert len(expr) == 1
            expr = expr[0]
        return expr

    def _prepare_setitem_multiple(self, expr):
        if isinstance(expr, str):
            expr = RhythmTreeParser()(expr)
        elif (
            isinstance(expr, list) and
            len(expr) == 1 and
            isinstance(expr[0], str)
        ):
            expr = RhythmTreeParser()(expr[0])
        return expr

    ### PRIVATE PROPERTIES ###

    def _get_contents_duration(self):
        """
        The total preprolated_duration of the children
        of a ``RhythmTreeContainer`` instance:

        >>> rtm = '(1 (1 (2 (1 1 1)) 2))'
        >>> tree = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]

        >>> tree._get_contents_duration()
        Duration(5, 1)

        >>> tree[1]._get_contents_duration()
        Duration(3, 1)

        Returns int.
        """
        return sum([x.preprolated_duration for x in self])

    @property
    def _leaf_class(self):
        return RhythmTreeLeaf

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
        """
        The node's RTM format:

        >>> rtm = '(1 ((1 (1 1)) (1 (1 1))))'
        >>> tree = abjad.rhythmtrees.RhythmTreeParser()(rtm)[0]
        >>> tree.rtm_format
        '(1 ((1 (1 1)) (1 (1 1))))'

        Returns string.
        """
        return '({!s} ({}))'.format(
            self.preprolated_duration,
            ' '.join([x.rtm_format for x in self]))


class RhythmTreeParser(Parser):
    r"""
    Rhythm-tree parser.

    ..  container:: example

        Abjad’s rhythm-tree parser parses a micro-language resembling Ircam’s
        RTM Lisp syntax, and generates a sequence of RhythmTree structures,
        which can be furthered manipulated by composers, before being converted
        into an Abjad score object:

        >>> parser = abjad.rhythmtrees.RhythmTreeParser()

        >>> string = '(3 (1 (1 ((2 (1 1 1)) 2 2 1))))'
        >>> rhythm_tree_list = parser(string)
        >>> rhythm_tree_container = rhythm_tree_list[0]
        >>> rhythm_tree_container.rtm_format
        '(3 (1 (1 ((2 (1 1 1)) 2 2 1))))'

        >>> abjad.f(rhythm_tree_container)
        abjad.rhythmtrees.RhythmTreeContainer(
            children=(
                abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=abjad.Duration(1, 1),
                    is_pitched=True,
                    ),
                abjad.rhythmtrees.RhythmTreeContainer(
                    children=(
                        abjad.rhythmtrees.RhythmTreeContainer(
                            children=(
                                abjad.rhythmtrees.RhythmTreeLeaf(
                                    preprolated_duration=abjad.Duration(1, 1),
                                    is_pitched=True,
                                    ),
                                abjad.rhythmtrees.RhythmTreeLeaf(
                                    preprolated_duration=abjad.Duration(1, 1),
                                    is_pitched=True,
                                    ),
                                abjad.rhythmtrees.RhythmTreeLeaf(
                                    preprolated_duration=abjad.Duration(1, 1),
                                    is_pitched=True,
                                    ),
                                ),
                            preprolated_duration=abjad.Duration(2, 1),
                            ),
                        abjad.rhythmtrees.RhythmTreeLeaf(
                            preprolated_duration=abjad.Duration(2, 1),
                            is_pitched=True,
                            ),
                        abjad.rhythmtrees.RhythmTreeLeaf(
                            preprolated_duration=abjad.Duration(2, 1),
                            is_pitched=True,
                            ), abjad.rhythmtrees.RhythmTreeLeaf(
                            preprolated_duration=abjad.Duration(1, 1),
                            is_pitched=True,
                            ),
                        ),
                    preprolated_duration=abjad.Duration(1, 1),
                    ),
                ),
            preprolated_duration=abjad.Duration(3, 1),
            )

        >>> base_duration = (1, 4)
        >>> component_list = rhythm_tree_container(base_duration)
        >>> tuplet = component_list[0]
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \tweak text #tuplet-number::calc-fraction-text
            \times 3/4 {
                c'2
                \times 4/7 {
                    \times 2/3 {
                        c'8
                        c'8
                        c'8
                    }
                    c'4
                    c'4
                    c'8
                }
            }

    """

    ### PUBLIC PROPERTIES ###

    @property
    def lexer_rules_object(self):
        return self

    @property
    def parser_rules_object(self):
        return self

    ### LEX SETUP ###

    tokens = (
        'DURATION',
        'LPAREN',
        'RPAREN'
    )

    t_LPAREN = r'\('
    t_RPAREN = r'\)'
    t_ignore = ' \n\t\r'

    ### YACC SETUP ###

    start = 'toplevel'

    ### LEX METHODS ###

    def t_DURATION(self, t):
        r'-?[1-9]\d*(/[1-9]\d*)?'
        import abjad
        parts = t.value.partition('/')
        if not parts[2]:
            t.value = abjad.Duration(int(parts[0]))
        else:
            numerator, denominator = int(parts[0]), int(parts[2])
            fraction = abjad.NonreducedFraction(numerator, denominator)
            preprolated_duration = abjad.Duration(fraction)
            if fraction.numerator == preprolated_duration.numerator:
                t.value = preprolated_duration
            else:
                t.value = fraction
        return t

    def t_error(self, t):
        print(("Illegal character '%s'" % t.value[0]))
        t.lexer.skip(1)

    def t_newline(self, t):
        r'\n+'
        t.lexer.lineno += t.value.count("\n")

    ### YACC METHODS ###

    def p_container__LPAREN__DURATION__node_list_closed__RPAREN(self, p):
        """
        container : LPAREN DURATION node_list_closed RPAREN
        """
        import abjad
        p[0] = abjad.rhythmtrees.RhythmTreeContainer(
            children=p[3],
            preprolated_duration=abs(p[2]),
            )

    def p_error(self, p):
        if p:
            print(("Syntax error at '%s'" % p.value))
        else:
            print("Syntax error at EOF")

    def p_leaf__INTEGER(self, p):
        """
        leaf : DURATION
        """
        import abjad
        p[0] = abjad.rhythmtrees.RhythmTreeLeaf(
            preprolated_duration=abs(p[1]),
            is_pitched=0 < p[1],
            )

    def p_node__container(self, p):
        """
        node : container
        """
        p[0] = p[1]

    def p_node__leaf(self, p):
        """
        node : leaf
        """
        p[0] = p[1]

    def p_node_list__node_list__node_list_item(self, p):
        """
        node_list : node_list node_list_item
        """
        p[0] = p[1] + [p[2]]

    def p_node_list__node_list_item(self, p):
        """
        node_list : node_list_item
        """
        p[0] = [p[1]]

    def p_node_list_closed__LPAREN__node_list__RPAREN(self, p):
        """
        node_list_closed : LPAREN node_list RPAREN
        """
        p[0] = p[2]

    def p_node_list_item__node(self, p):
        """
        node_list_item : node
        """
        p[0] = p[1]

    def p_toplevel__EMPTY(self, p):
        """
        toplevel :
        """
        p[0] = []

    def p_toplevel__toplevel__node(self, p):
        """
        toplevel : toplevel node
        """
        p[0] = p[1] + [p[2]]


def parse_rtm_syntax(rtm):
    r"""
    Parses RTM syntax.

    ..  container:: example

        Parses tuplet:

        >>> rtm = '(1 (1 (1 (1 1)) 1))'
        >>> tuplet = abjad.rhythmtrees.parse_rtm_syntax(rtm)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \times 2/3 {
                c'8
                c'16
                c'16
                c'8
            }

    ..  container:: example

        Also supports fractional durations:

        >>> rtm = '(3/4 (1 1/2 (4/3 (1 -1/2 1))))'
        >>> tuplet = abjad.rhythmtrees.parse_rtm_syntax(rtm)
        >>> abjad.show(tuplet) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(tuplet)
            \tweak text #tuplet-number::calc-fraction-text
            \times 9/17 {
                c'8
                c'16
                \tweak edge-height #'(0.7 . 0)
                \times 8/15 {
                    c'8
                    r16
                    c'8
                }
            }

    Returns tuplet or container.
    """
    result = RhythmTreeParser()(rtm)
    container = core.Container()
    for node in result:
        tuplet = node((1, 4))
        # following line added 2012-08-01. tb.
        tuplet = tuplet[0]
        if tuplet.trivial():
            container.extend(tuplet[:])
        else:
            container.append(tuplet)
    if len(container) == 1:
        return container[0]
    return container
