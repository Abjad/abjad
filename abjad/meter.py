"""
Tools for modeling musical meter.
"""
import bisect
import collections
import typing

import uqbar.graphs

from . import _inspect, _iterate, markups, math, mutate, rhythmtrees
from .duration import Duration, Multiplier, NonreducedFraction, Offset
from .indicators.TimeSignature import TimeSignature
from .lilypondfile import LilyPondFile
from .new import new
from .parentage import Parentage
from .score import Chord, Container, Note, Rest, Skip, Tuplet
from .select import LogicalTie, Selection
from .sequence import Sequence
from .storage import FormatSpecification, StorageFormatManager
from .timespan import OffsetCounter, Timespan, TimespanList
from .typedcollections import TypedList


class Meter:
    """
    Meter.

    Meter models a common practice understanding of beats and other levels of
    rhythmic organization structured as a tree. Meter structure corresponds to
    the monotonically increasing sequence of factors in the numerator of a
    given time signature. Successively deeper levels of the tree divide time by
    successive factors.

    ..  container:: example

        Duple meter:

        >>> meter = abjad.Meter((2, 4))
        >>> meter
        Meter('(2/4 (1/4 1/4))')
        >>> print(meter.pretty_rtm_format)
        (2/4 (
            1/4
            1/4))

        >>> abjad.graph(meter) # doctest: +SKIP

        ``2/4`` comprises two beats.

    ..  container:: example

        Triple meter:

        >>> meter = abjad.Meter((3, 4))
        >>> print(meter.pretty_rtm_format)
        (3/4 (
            1/4
            1/4
            1/4))

        >>> abjad.graph(meter) # doctest: +SKIP

        ``3/4`` comprises three beats.

    ..  container:: example

        Quadruple meter:

        >>> meter = abjad.Meter((4, 4))
        >>> meter
        Meter('(4/4 (1/4 1/4 1/4 1/4))')
        >>> print(meter.pretty_rtm_format)
        (4/4 (
            1/4
            1/4
            1/4
            1/4))

        >>> abjad.graph(meter) # doctest: +SKIP

        ``4/4`` comprises four beats.

    ..  container:: example

        Compound triple meter:

        >>> meter = abjad.Meter((6, 8))
        >>> print(meter.pretty_rtm_format)
        (6/8 (
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))))

        >>> abjad.graph(meter) # doctest: +SKIP

        ``6/8`` comprises two beats of three parts each.

    ..  container:: example

        Another compound triple meter:

        >>> meter = abjad.Meter((12, 8))
        >>> print(meter.pretty_rtm_format)
        (12/8 (
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))))

        >>> abjad.graph(meter) # doctest: +SKIP

        ``12/8`` comprises four beats of three parts each.

    ..  container:: example

        An asymmetric meter:

        >>> meter = abjad.Meter((5, 4))
        >>> print(meter.pretty_rtm_format)
        (5/4 (
            (3/4 (
                1/4
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

        >>> abjad.graph(meter) # doctest: +SKIP

        ``5/4`` comprises two unequal beats. By default unequal beats
        are arranged from greatest to least.

    ..  container:: example

        Another asymmetric meter:

        >>> meter = abjad.Meter((7, 4))
        >>> print(meter.pretty_rtm_format)
        (7/4 (
            (3/4 (
                1/4
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

        >>> abjad.graph(meter) # doctest: +SKIP

        ``7/4`` comprises three unequal beats. Beats are arranged from
        greatest to least by default.

    ..  container:: example

        The same asymmetric meter structured differently:

        >>> meter = abjad.Meter(
        ...     (7, 4),
        ...     increase_monotonic=True,
        ...     )
        >>> print(meter.pretty_rtm_format)
        (7/4 (
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))))

        >>> abjad.graph(meter) # doctest: +SKIP

        ``7/4`` with beats arragned from least to greatest.

    ..  container:: example

        Meter interpreted by default as containing two compound beats:

        >>> meter = abjad.Meter((6, 4))
        >>> meter
        Meter('(6/4 ((3/4 (1/4 1/4 1/4)) (3/4 (1/4 1/4 1/4))))')
        >>> print(meter.pretty_rtm_format)
        (6/4 (
            (3/4 (
                1/4
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))))

        >>> abjad.graph(meter) # doctest: +SKIP

        Same meter customized to contain four compound beats:

        >>> parser = abjad.rhythmtrees.RhythmTreeParser()
        >>> meter = abjad.Meter('(6/4 ((3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8))))')
        >>> meter
        Meter('(6/4 ((3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8)) (3/8 (1/8 1/8 1/8))))')
        >>> print(meter.pretty_rtm_format)
        (6/4 (
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))))

        >>> abjad.graph(meter) # doctest: +SKIP

    Prime divisions greater than ``3`` are converted to sequences of ``2``
    and ``3`` summing to that prime. Summands are arranged from greatest
    to least by default. This means that ``5`` becomes ``3+2`` and ``7``
    becomes ``3+2+2`` in the examples above.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_increase_monotonic",
        "_denominator",
        "_numerator",
        "_preferred_boundary_depth",
        "_root_node",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        argument=None,
        increase_monotonic=None,
        preferred_boundary_depth=None,
    ):
        argument = argument or (4, 4)
        assert isinstance(preferred_boundary_depth, (int, type(None)))
        self._preferred_boundary_depth = preferred_boundary_depth

        def recurse(node, factors, denominator, increase_monotonic):
            if factors:
                factor, factors = factors[0], factors[1:]
                preprolated_duration = node.preprolated_duration.__div__(factor)
                # if factor in (2, 3, 4, 5):
                if factor in (2, 3, 4):
                    if factors:
                        for _ in range(factor):
                            child = rhythmtrees.RhythmTreeContainer(
                                preprolated_duration=preprolated_duration
                            )
                            node.append(child)
                            recurse(child, factors, denominator, increase_monotonic)
                    else:
                        for _ in range(factor):
                            node.append(
                                rhythmtrees.RhythmTreeLeaf(
                                    preprolated_duration=(1, denominator)
                                )
                            )
                else:
                    parts = [3]
                    total = 3
                    while total < factor:
                        if not increase_monotonic:
                            parts.append(2)
                        else:
                            parts.insert(0, 2)
                        total += 2
                    for part in parts:
                        grouping = rhythmtrees.RhythmTreeContainer(
                            preprolated_duration=part * preprolated_duration
                        )
                        if factors:
                            for _ in range(part):
                                child = rhythmtrees.RhythmTreeContainer(
                                    preprolated_duration=preprolated_duration
                                )
                                grouping.append(child)
                                recurse(
                                    child,
                                    factors,
                                    denominator,
                                    increase_monotonic,
                                )
                        else:
                            for _ in range(part):
                                grouping.append(
                                    rhythmtrees.RhythmTreeLeaf(
                                        preprolated_duration=(1, denominator)
                                    )
                                )
                        node.append(grouping)
            else:
                node.extend(
                    [
                        rhythmtrees.RhythmTreeLeaf(
                            preprolated_duration=(1, denominator)
                        )
                        for _ in range(node.preprolated_duration.numerator)
                    ]
                )

        increase_monotonic = bool(increase_monotonic)
        try:
            numerator = argument.numerator
            denominator = argument.denominator
            is_fraction_like = True
        except AttributeError:
            is_fraction_like = False
        if isinstance(argument, type(self)):
            root = argument.root_node
            numerator, denominator = argument.numerator, argument.denominator
            increase_monotonic = argument.increase_monotonic
        elif isinstance(argument, (str, rhythmtrees.RhythmTreeContainer)):
            if isinstance(argument, str):
                parsed = rhythmtrees.RhythmTreeParser()(argument)
                assert len(parsed) == 1
                root = parsed[0]
            else:
                root = argument
            for node in [root] + list(root.depth_first()):
                assert node.prolation == 1
            numerator = root.preprolated_duration.numerator
            denominator = root.preprolated_duration.denominator
        elif is_fraction_like or isinstance(argument, tuple):
            if isinstance(argument, tuple):
                fraction = NonreducedFraction(argument)
            else:
                fraction = NonreducedFraction(argument.numerator, argument.denominator)
            numerator, denominator = fraction.numerator, fraction.denominator
            factors = math.factors(numerator)
            # group two nested levels of 2s into a 4
            if 1 < len(factors) and factors[0] == factors[1] == 2:
                factors[0:2] = [4]
            root = rhythmtrees.RhythmTreeContainer(preprolated_duration=fraction)
            recurse(root, factors, denominator, increase_monotonic)
        else:
            name = type(self).__name__
            raise ValueError(f"can not initialize {name}: {argument!r}.")

        self._root_node = root
        self._numerator = numerator
        self._denominator = denominator
        self._increase_monotonic = increase_monotonic

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a meter with an rtm format equal to that
        of this meter.

        Returns true or false.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __graph__(self, **keywords):
        """
        Gets Graphviz format of meter.

        ..  container:: example

            Graphs ``7/4``:

            >>> meter = abjad.Meter((7, 4))
            >>> meter_graph = meter.__graph__()
            >>> abjad.graph(meter_graph) # doctest: +SKIP

            ..  docs::

                >>> print(format(meter_graph, 'graphviz'))
                digraph G {
                    graph [bgcolor=transparent,
                        fontname=Arial,
                        penwidth=2,
                        truecolor=true];
                    node [fontname=Arial,
                        fontsize=12,
                        penwidth=2];
                    edge [penwidth=2];
                    node_0 [label="7/4",
                        shape=triangle];
                    node_1 [label="3/4",
                        shape=triangle];
                    node_2 [label="1/4",
                        shape=box];
                    node_3 [label="1/4",
                        shape=box];
                    node_4 [label="1/4",
                        shape=box];
                    node_5 [label="2/4",
                        shape=triangle];
                    node_6 [label="1/4",
                        shape=box];
                    node_7 [label="1/4",
                        shape=box];
                    node_8 [label="2/4",
                        shape=triangle];
                    node_9 [label="1/4",
                        shape=box];
                    node_10 [label="1/4",
                        shape=box];
                    subgraph cluster_offsets {
                        graph [style=rounded];
                        node_11_0 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 0 | <f_0_1> +++ }",
                            shape=Mrecord,
                            style=filled];
                        node_11_1 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 1/4 | <f_0_1> + }",
                            shape=Mrecord,
                            style=filled];
                        node_11_2 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 1/2 | <f_0_1> + }",
                            shape=Mrecord,
                            style=filled];
                        node_11_3 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 3/4 | <f_0_1> ++ }",
                            shape=Mrecord,
                            style=filled];
                        node_11_4 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 1 | <f_0_1> + }",
                            shape=Mrecord,
                            style=filled];
                        node_11_5 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 5/4 | <f_0_1> ++ }",
                            shape=Mrecord,
                            style=filled];
                        node_11_6 [color=white,
                            fillcolor=black,
                            fontcolor=white,
                            fontname="Arial bold",
                            label="{ <f_0_0> 3/2 | <f_0_1> + }",
                            shape=Mrecord,
                            style=filled];
                        node_11_7 [label="{ <f_0_0> 7/4 | <f_0_1> +++ }",
                            shape=Mrecord];
                    }
                    node_0 -> node_1;
                    node_0 -> node_5;
                    node_0 -> node_8;
                    node_1 -> node_2;
                    node_1 -> node_3;
                    node_1 -> node_4;
                    node_2 -> node_11_0 [style=dotted];
                    node_2 -> node_11_1 [style=dotted];
                    node_3 -> node_11_1 [style=dotted];
                    node_3 -> node_11_2 [style=dotted];
                    node_4 -> node_11_2 [style=dotted];
                    node_4 -> node_11_3 [style=dotted];
                    node_5 -> node_6;
                    node_5 -> node_7;
                    node_6 -> node_11_3 [style=dotted];
                    node_6 -> node_11_4 [style=dotted];
                    node_7 -> node_11_4 [style=dotted];
                    node_7 -> node_11_5 [style=dotted];
                    node_8 -> node_9;
                    node_8 -> node_10;
                    node_9 -> node_11_5 [style=dotted];
                    node_9 -> node_11_6 [style=dotted];
                    node_10 -> node_11_6 [style=dotted];
                    node_10 -> node_11_7 [style=dotted];
                }

        Returns Graphviz graph.
        """

        def make_offset_node(offset, leaf_one=None, leaf_two=None, is_last=False):
            if not is_last:
                offset_node = uqbar.graphs.Node(
                    attributes={
                        "shape": "Mrecord",
                        "style": "filled",
                        "color": "white",
                        "fontname": "Arial bold",
                        "fontcolor": "white",
                        "fillcolor": "black",
                    }
                )
            else:
                offset_node = uqbar.graphs.Node(attributes={"shape": "Mrecord"})
            offset_field = uqbar.graphs.RecordField(label=str(offset))
            weight_field = uqbar.graphs.RecordField(label="+" * offsets[offset])
            group = uqbar.graphs.RecordGroup()
            group.extend([offset_field, weight_field])
            offset_node.append(group)
            offset_subgraph.append(offset_node)
            leaf_one_node = node_mapping[leaf_one]
            edge = uqbar.graphs.Edge(attributes={"style": "dotted"})
            edge.attach(leaf_one_node, offset_node)
            if leaf_two:
                leaf_two_node = node_mapping[leaf_two]
                edge = uqbar.graphs.Edge(attributes={"style": "dotted"})
                edge.attach(leaf_two_node, offset_node)

        offsets = MetricAccentKernel.count_offsets(
            Sequence(self.depthwise_offset_inventory).flatten(depth=-1)
        )
        graph = uqbar.graphs.Graph(
            name="G",
            attributes={
                "bgcolor": "transparent",
                "fontname": "Arial",
                "penwidth": 2,
                "truecolor": True,
            },
            edge_attributes={"penwidth": 2},
            node_attributes={"fontname": "Arial", "fontsize": 12, "penwidth": 2},
        )
        node_mapping = {}
        root = self._root_node
        nodes = [root] + list(root.depth_first())
        leaves = [_ for _ in nodes if not hasattr(_, "children")]
        for node in nodes:
            graphviz_node = uqbar.graphs.Node()
            graphviz_node.attributes["label"] = str(node.preprolated_duration)
            if isinstance(node, rhythmtrees.RhythmTreeContainer):
                graphviz_node.attributes["shape"] = "triangle"
            else:
                graphviz_node.attributes["shape"] = "box"
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node.parent is not None:
                uqbar.graphs.Edge().attach(
                    node_mapping[node.parent], node_mapping[node]
                )
        offset = leaves[0].start_offset
        offset_subgraph = uqbar.graphs.Graph(
            name="cluster_offsets", attributes={"style": "rounded"}
        )
        graph.append(offset_subgraph)
        make_offset_node(offset, leaves[0])
        for one, two in Sequence(leaves).nwise():
            offset = one.stop_offset
            make_offset_node(offset, one, two)
        offset = leaves[-1].stop_offset
        make_offset_node(offset, leaves[-1], is_last=True)
        return graph

    def __hash__(self):
        """
        Hashes meter.

        Returns integer.
        """
        return super().__hash__()

    def __iter__(self):
        """
        Iterates meter.

        ..  container:: example

            Iterates ``5/4``:


                >>> meter = abjad.Meter((5, 4))
                >>> for pair in meter:
                ...    pair
                ...
                (NonreducedFraction(0, 4), NonreducedFraction(1, 4))
                (NonreducedFraction(1, 4), NonreducedFraction(2, 4))
                (NonreducedFraction(2, 4), NonreducedFraction(3, 4))
                (NonreducedFraction(0, 4), NonreducedFraction(3, 4))
                (NonreducedFraction(3, 4), NonreducedFraction(4, 4))
                (NonreducedFraction(4, 4), NonreducedFraction(5, 4))
                (NonreducedFraction(3, 4), NonreducedFraction(5, 4))
                (NonreducedFraction(0, 4), NonreducedFraction(5, 4))

        Yields pairs.
        """

        def recurse(node):
            result = []
            for child in node:
                if isinstance(child, rhythmtrees.RhythmTreeLeaf):
                    result.append(child)
                else:
                    result.extend(recurse(child))
            result.append(node)
            return result

        result = recurse(self.root_node)
        for node in result:
            start_offset = NonreducedFraction(node.start_offset)
            start_offset = start_offset.with_denominator(self.denominator)
            stop_offset = NonreducedFraction(node.stop_offset)
            stop_offset = stop_offset.with_denominator(self.denominator)
            yield start_offset, stop_offset

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __str__(self) -> str:
        """
        Gets string representation of meter.

        ..  container:: example

            Gets string representation of meters over ``8``:

            >>> for numerator in range(1, 9):
            ...     meter = abjad.Meter((numerator, 8))
            ...     print(str(meter))
            1/8
            2/8
            3/8
            4/8
            5/8
            6/8
            7/8
            8/8

        """
        return f"{self.numerator}/{self.denominator}"

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.rtm_format],
            storage_format_keyword_names=[],
        )

    ### PUBLIC PROPERTIES ###

    @property
    def denominator(self):
        """
        Gets denominator of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> meter.denominator
            4

        Returns positive integer.
        """
        return self._denominator

    @property
    def depthwise_offset_inventory(self):
        """
        Gets depthwise offset inventory of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> for depth, offsets in enumerate(
            ...     meter.depthwise_offset_inventory):
            ...     print(depth, offsets)
            0 (Offset((0, 1)), Offset((7, 4)))
            1 (Offset((0, 1)), Offset((3, 4)), Offset((5, 4)), Offset((7, 4)))
            2 (Offset((0, 1)), Offset((1, 4)), Offset((1, 2)), Offset((3, 4)), Offset((1, 1)), Offset((5, 4)), Offset((3, 2)), Offset((7, 4)))

        Returns dictionary.
        """
        inventory = []
        all_offsets = set()
        all_offsets.add(Offset(self.numerator, self.denominator))
        for depth, nodes in sorted(self.root_node._depthwise_inventory().items()):
            for node in nodes:
                all_offsets.add(Offset(node.start_offset))
            inventory.append(tuple(sorted(all_offsets)))
        return tuple(inventory)

    @property
    def duration(self):
        """
        Gets duration of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> meter.duration
            Duration(7, 4)

        Returns duration.
        """
        return Duration(self.numerator, self.denominator)

    @property
    def implied_time_signature(self):
        """
        Gets implied time signature of meter.

        ..  container:: example

            >>> abjad.Meter((4, 4)).implied_time_signature
            TimeSignature((4, 4))

        Returns time signature.
        """
        return TimeSignature(self.root_node.preprolated_duration)

    @property
    def increase_monotonic(self) -> typing.Optional[bool]:
        """
        Is true when meter divides large primes into collections of ``2``
        and ``3`` that increase monotonically.

        ..  container:: example

            An asymmetric meter with beats arranged greatest to least:

            >>> meter = abjad.Meter(
            ...     (7, 4),
            ...     increase_monotonic=False,
            ...     )

            >>> meter.increase_monotonic
            False

            >>> print(meter.pretty_rtm_format)
            (7/4 (
                (3/4 (
                    1/4
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))))

            This is default beahvior.

        ..  container:: example

            The same asymmetric meter with unequal beats arranged least to
            greatest:

            >>> meter = abjad.Meter(
            ...     (7, 4),
            ...     increase_monotonic=True
            ...     )

            >>> meter.increase_monotonic
            True

            >>> print(meter.pretty_rtm_format)
            (7/4 (
                (2/4 (
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))
                (3/4 (
                    1/4
                    1/4
                    1/4))))

        """
        return self._increase_monotonic

    @property
    def is_compound(self):
        """
        Is true when meter is compound.

        ..  container:: example

            Compound meters written over ``4``:

            >>> for numerator in range(1, 13):
            ...     meter = abjad.Meter((numerator, 4))
            ...     string = True if meter.is_compound else ''
            ...     print(str(meter), string)
            ...
            1/4
            2/4
            3/4
            4/4
            5/4
            6/4     True
            7/4
            8/4
            9/4     True
            10/4
            11/4
            12/4    True

        ..  container:: example

            Compound meters written over ``8``:

            >>> for numerator in range(1, 13):
            ...     meter = abjad.Meter((numerator, 8))
            ...     string = True if meter.is_compound else ''
            ...     print(str(meter), string)
            ...
            1/8
            2/8
            3/8
            4/8
            5/8
            6/8     True
            7/8
            8/8
            9/8     True
            10/8
            11/8
            12/8    True

        Compound meters defined equal to those meters with a numerator
        divisible by ``3`` (but not equal to ``3``).

        Returns true or false.
        """
        if 3 in math.divisors(self.numerator):
            if not self.numerator == 3:
                return True
        return False

    @property
    def is_simple(self):
        """
        Is true when meter is simple.

        ..  container:: example

            Simple meters written over ``4``:

            >>> for numerator in range(1, 13):
            ...     meter = abjad.Meter((numerator, 4))
            ...     string = True if meter.is_simple else ''
            ...     print(str(meter), string)
            ...
            1/4     True
            2/4     True
            3/4     True
            4/4     True
            5/4     True
            6/4
            7/4     True
            8/4     True
            9/4
            10/4    True
            11/4    True
            12/4

        ..  container:: example

            Simple meters written over ``8``:

            >>> for numerator in range(1, 13):
            ...     meter = abjad.Meter((numerator, 8))
            ...     string = True if meter.is_simple else ''
            ...     print(str(meter), string)
            ...
            1/8     True
            2/8     True
            3/8     True
            4/8     True
            5/8     True
            6/8
            7/8     True
            8/8     True
            9/8
            10/8    True
            11/8    True
            12/8

        Simple meters defined equal to those meters with a numerator
        not divisible by ``3``.

        Meters with numerator equal to ``3`` are also defined as simple.

        Returns true or false.
        """
        return not self.is_compound

    @property
    def numerator(self):
        """
        Gets numerator of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> meter.numerator
            7

        Returns positive integer.
        """
        return self._numerator

    @property
    def pair(self):
        """
        Gets pair of numerator and denominator of meter.

        ..  container:: example

            >>> meter = abjad.Meter((6, 4))
            >>> meter.pair
            (6, 4)

        Returns pair.
        """
        return (self.numerator, self.denominator)

    @property
    def preferred_boundary_depth(self):
        """
        Gets preferred boundary depth of meter.

        ..  container:: example

            No preferred boundary depth:

            >>> abjad.Meter((6, 8)).preferred_boundary_depth is None
            True

        ..  container:: example

            Customized preferred boundary depth:

            >>> meter = abjad.Meter(
            ...     (6, 8),
            ...     preferred_boundary_depth=1,
            ...     )
            >>> meter.preferred_boundary_depth
            1

        Used by ``abjad.Meter.rewrite_meter()``.

        Defaults to none.

        Set to integer or none.

        Returns integer or none.
        """
        return self._preferred_boundary_depth

    @property
    def pretty_rtm_format(self):
        """
        Gets pretty RTM format of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> print(meter.pretty_rtm_format)
            (7/4 (
                (3/4 (
                    1/4
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))))

        Returns string.
        """
        return self.root_node.pretty_rtm_format

    @property
    def root_node(self):
        """
        Gets root node of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> print(abjad.storage(meter.root_node))
            abjad.rhythmtrees.RhythmTreeContainer(
                children=(
                    abjad.rhythmtrees.RhythmTreeContainer(
                        children=(
                            abjad.rhythmtrees.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            abjad.rhythmtrees.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            abjad.rhythmtrees.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            ),
                        preprolated_duration=abjad.NonreducedFraction(3, 4),
                        ),
                    abjad.rhythmtrees.RhythmTreeContainer(
                        children=(
                            abjad.rhythmtrees.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            abjad.rhythmtrees.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            ),
                        preprolated_duration=abjad.NonreducedFraction(2, 4),
                        ),
                    abjad.rhythmtrees.RhythmTreeContainer(
                        children=(
                            abjad.rhythmtrees.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            abjad.rhythmtrees.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            ),
                        preprolated_duration=abjad.NonreducedFraction(2, 4),
                        ),
                    ),
                preprolated_duration=abjad.NonreducedFraction(7, 4),
                )

        Returns rhythm tree node.
        """
        return self._root_node

    @property
    def rtm_format(self):
        """
        Gets RTM format of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> meter.rtm_format
            '(7/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'

        Returns string.
        """
        return self._root_node.rtm_format

    ### PUBLIC METHODS ###

    @staticmethod
    def fit_meters(
        argument,
        meters,
        denominator=32,
        discard_final_orphan_downbeat=True,
        maximum_run_length=None,
        starting_offset=None,
    ):
        """
        Finds the best-matching sequence of meters for the offsets
        contained in ``argument``.

        ..  container:: example

            >>> meters = [(3, 4), (4, 4), (5, 4)]
            >>> meters = [abjad.Meter(_) for _ in meters]

        ..  container:: example

            Matches a series of hypothetical ``4/4`` measures:

            >>> argument = [(0, 4), (4, 4), (8, 4), (12, 4), (16, 4)]
            >>> for meter in abjad.Meter.fit_meters(argument, meters):
            ...     print(meter.implied_time_signature)
            ...
            4/4
            4/4
            4/4
            4/4

        ..  container:: example

            Matches a series of hypothetical ``5/4`` measures:

            >>> argument = [(0, 4), (3, 4), (5, 4), (10, 4), (15, 4), (20, 4)]
            >>> for meter in abjad.Meter.fit_meters(argument, meters):
            ...     print(meter.implied_time_signature)
            ...
            3/4
            4/4
            3/4
            5/4
            5/4

        Coerces offsets from ``argument`` via
        ``MetricAccentKernel.count_offsets()``.

        Coerces Meters from ``meters`` via ``MeterList``.

        Returns list.
        """
        session = _MeterFittingSession(
            kernel_denominator=denominator,
            maximum_run_length=maximum_run_length,
            meters=meters,
            offset_counter=argument,
        )
        meters = session()
        return meters

    def generate_offset_kernel_to_denominator(self, denominator, normalize=True):
        r"""
        Generates a dictionary of all offsets in a meter up
        to ``denominator``.

        Keys are the offsets and the values are the normalized weights of
        those offsets.

        ..  container:: example

            >>> meter = abjad.Meter((4, 4))
            >>> kernel = meter.generate_offset_kernel_to_denominator(8)
            >>> for offset, weight in sorted(kernel.kernel.items()):
            ...     print(f"{offset!s}\t{weight!s}")
            ...
            0       3/16
            1/8     1/16
            1/4     1/8
            3/8     1/16
            1/2     1/8
            5/8     1/16
            3/4     1/8
            7/8     1/16
            1       3/16

        This is useful for testing how strongly a collection of offsets
        responds to a given meter.

        Returns dictionary.
        """
        assert math.is_positive_integer_power_of_two(denominator // self.denominator)
        inventory = list(self.depthwise_offset_inventory)
        old_flag_count = Duration(1, self.denominator).flag_count
        new_flag_count = Duration(1, denominator).flag_count
        extra_depth = new_flag_count - old_flag_count
        for _ in range(extra_depth):
            old_offsets = inventory[-1]
            new_offsets = []
            for first, second in Sequence(old_offsets).nwise():
                new_offsets.append(first)
                new_offsets.append((first + second) / 2)
            new_offsets.append(old_offsets[-1])
            inventory.append(tuple(new_offsets))
        total = 0
        kernel = {}
        for offsets in inventory:
            for offset in offsets:
                if offset not in kernel:
                    kernel[offset] = 0
                kernel[offset] += 1
                total += 1
        if normalize:
            for offset, response in kernel.items():
                kernel[offset] = Multiplier(response, total)
        return MetricAccentKernel(kernel)

    def rewrite_meter(
        components,
        meter,
        boundary_depth=None,
        initial_offset=None,
        maximum_dot_count=None,
        rewrite_tuplets=True,
    ):
        r"""
        Rewrites the contents of logical ties in an expression to match ``meter``.

        ..  container:: example

            Rewrites the contents of a measure in a staff using the default
            meter for that measure's time signature:

            >>> lily_string = "| 2/4 c'2 ~ |"
            >>> lily_string += "| 4/4 c'32 d'2.. ~ d'16 e'32 ~ |"
            >>> lily_string += "| 2/4 e'2 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff[:] = container
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 2/4
                        c'2
                        ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'2..
                        ~
                        d'16
                        e'32
                        ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

            >>> meter = abjad.Meter((4, 4))
            >>> print(meter.pretty_rtm_format)
            (4/4 (
                1/4
                1/4
                1/4
                1/4))

            >>> abjad.Meter.rewrite_meter(staff[1][:], meter)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 2/4
                        c'2
                        ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'8..
                        ~
                        d'2
                        ~
                        d'8..
                        e'32
                        ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

        ..  container:: example

            Rewrites the contents of a measure in a staff using a custom meter:

            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff[:] = container
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 2/4
                        c'2
                        ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'2..
                        ~
                        d'16
                        e'32
                        ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

            >>> rtm = '(4/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'
            >>> meter = abjad.Meter(rtm)
            >>> print(meter.pretty_rtm_format) # doctest: +SKIP
            (4/4 (
                (2/4 (
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))))

            >>> abjad.Meter.rewrite_meter(staff[1][:], meter)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 2/4
                        c'2
                        ~
                    }
                    {
                        \time 4/4
                        c'32
                        d'4...
                        ~
                        d'4...
                        e'32
                        ~
                    }
                    {
                        \time 2/4
                        e'2
                    }
                }

        ..  container:: example

            Limit the maximum number of dots per leaf using
            ``maximum_dot_count``:

            >>> lily_string = "| 3/4 c'32 d'8 e'8 fs'4... |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'8
                        e'8
                        fs'4...
                    }
                }

            Without constraining the ``maximum_dot_count``:

            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(
            ...     measure[0],
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.Meter.rewrite_meter(measure[:], time_signature)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'16.
                        ~
                        d'32
                        e'16.
                        ~
                        e'32
                        fs'4...
                    }
                }

            Constraining the ``maximum_dot_count`` to ``2``:

            >>> lily_string = "| 3/4 c'32 d'8 e'8 fs'4... |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(
            ...     measure[0],
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.Meter.rewrite_meter(
            ...     measure[:],
            ...     time_signature,
            ...     maximum_dot_count=2,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'16.
                        ~
                        d'32
                        e'16.
                        ~
                        e'32
                        fs'8..
                        ~
                        fs'4
                    }
                }

            Constraining the ``maximum_dot_count`` to ``1``:

            >>> lily_string = "| 3/4 c'32 d'8 e'8 fs'4... |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(
            ...     measure[0],
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.Meter.rewrite_meter(
            ...     measure[:],
            ...     time_signature,
            ...     maximum_dot_count=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'16.
                        ~
                        d'32
                        e'16.
                        ~
                        e'32
                        fs'16.
                        ~
                        fs'8
                        ~
                        fs'4
                    }
                }

            Constraining the ``maximum_dot_count`` to ``0``:

            >>> lily_string = "| 3/4 c'32 d'8 e'8 fs'4... |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(
            ...     measure[0],
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.Meter.rewrite_meter(
            ...     measure[:],
            ...     time_signature,
            ...     maximum_dot_count=0,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 3/4
                        c'32
                        d'16
                        ~
                        d'32
                        ~
                        d'32
                        e'16
                        ~
                        e'32
                        ~
                        e'32
                        fs'16
                        ~
                        fs'32
                        ~
                        fs'8
                        ~
                        fs'4
                    }
                }

        ..  container:: example

            Split logical ties at different depths of the ``Meter``, if those
            logical ties cross any offsets at that depth, but do not also both
            begin and end at any of those offsets.

            Consider the default meter for ``9/8``:

            >>> meter = abjad.Meter((9, 8))
            >>> print(meter.pretty_rtm_format)
            (9/8 (
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))))

            We can establish that meter without specifying
            a ``boundary_depth``:

            >>> lily_string = "| 9/8 c'2 d'2 e'8 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 9/8
                        c'2
                        d'2
                        e'8
                    }
                }

            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(
            ...     measure[0],
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.Meter.rewrite_meter(measure[:], time_signature)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 9/8
                        c'2
                        d'4
                        ~
                        d'4
                        e'8
                    }
                }

            With a ``boundary_depth`` of ``1`` logical ties which cross any
            offsets created by nodes with a depth of ``1`` in this Meter's rhythm
            tree - i.e.  ``0/8`` ``3/8`` ``6/8`` and ``9/8`` - which do not also
            begin and end at any of those offsets, will be split:

            >>> lily_string = "| 9/8 c'2 d'2 e'8 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(
            ...     measure[0],
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.Meter.rewrite_meter(
            ...     measure[:],
            ...     time_signature,
            ...     boundary_depth=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 9/8
                        c'4.
                        ~
                        c'8
                        d'4
                        ~
                        d'4
                        e'8
                    }
                }

            For this ``9/8`` meter, and this input notation, A ``boundary_depth``
            of ``2`` causes no change, as all logical ties already align to
            multiples of ``1/8``

            >>> lily_string = "| 9/8 c'2 d'2 e'8 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(
            ...     measure[0],
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.Meter.rewrite_meter(
            ...     measure[:],
            ...     time_signature,
            ...     boundary_depth=2,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 9/8
                        c'2
                        d'4
                        ~
                        d'4
                        e'8
                    }
                }

        ..  container:: example

            Comparison of ``3/4`` and ``6/8`` at ``boundary_depths`` of 0 and 1:

            >>> triple = "| 3/4 2 4 || 3/4 4 2 || 3/4 4. 4. |"
            >>> triple += "| 3/4 2 ~ 8 8 || 3/4 8 8 ~ 2 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(triple)
            >>> staff_1 = abjad.Staff()
            >>> staff_1[:] = container
            >>> duples = "| 6/8 2 4 || 6/8 4 2 || 6/8 4. 4. |"
            >>> duples += "| 6/8 2 ~ 8 8 || 6/8 8 8 ~ 2 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(duples)
            >>> staff_2 = abjad.Staff()
            >>> staff_2[:] = container
            >>> score = abjad.Score([staff_1, staff_2])

            In order to see the different time signatures on each staff,
            we need to move some engravers from the Score context to the
            Staff context:

            >>> engravers = [
            ...     'Timing_translator',
            ...     'Time_signature_engraver',
            ...     'Default_bar_line_engraver',
            ...     ]
            >>> score.remove_commands.extend(engravers)
            >>> score[0].consists_commands.extend(engravers)
            >>> score[1].consists_commands.extend(engravers)
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                \with
                {
                    \remove Timing_translator
                    \remove Time_signature_engraver
                    \remove Default_bar_line_engraver
                }
                <<
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 3/4
                            c'2
                            c'4
                        }
                        {
                            \time 3/4
                            c'4
                            c'2
                        }
                        {
                            \time 3/4
                            c'4.
                            c'4.
                        }
                        {
                            \time 3/4
                            c'2
                            ~
                            c'8
                            c'8
                        }
                        {
                            \time 3/4
                            c'8
                            c'8
                            ~
                            c'2
                        }
                    }
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 6/8
                            c'2
                            c'4
                        }
                        {
                            \time 6/8
                            c'4
                            c'2
                        }
                        {
                            \time 6/8
                            c'4.
                            c'4.
                        }
                        {
                            \time 6/8
                            c'2
                            ~
                            c'8
                            c'8
                        }
                        {
                            \time 6/8
                            c'8
                            c'8
                            ~
                            c'2
                        }
                    }
                >>

            Here we establish a meter without specifying any boundary depth:

            >>> for staff in score:
            ...     for container in staff:
            ...         leaf = abjad.get.leaf(container, 0)
            ...         time_signature = abjad.get.indicator(
            ...             leaf,
            ...             abjad.TimeSignature
            ...             )
            ...         abjad.Meter.rewrite_meter(container[:], time_signature)
            ...
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                \with
                {
                    \remove Timing_translator
                    \remove Time_signature_engraver
                    \remove Default_bar_line_engraver
                }
                <<
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 3/4
                            c'2
                            c'4
                        }
                        {
                            \time 3/4
                            c'4
                            c'2
                        }
                        {
                            \time 3/4
                            c'4.
                            c'4.
                        }
                        {
                            \time 3/4
                            c'2
                            ~
                            c'8
                            c'8
                        }
                        {
                            \time 3/4
                            c'8
                            c'8
                            ~
                            c'2
                        }
                    }
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 6/8
                            c'2
                            c'4
                        }
                        {
                            \time 6/8
                            c'4
                            c'2
                        }
                        {
                            \time 6/8
                            c'4.
                            c'4.
                        }
                        {
                            \time 6/8
                            c'4.
                            ~
                            c'4
                            c'8
                        }
                        {
                            \time 6/8
                            c'8
                            c'4
                            ~
                            c'4.
                        }
                    }
                >>

            Here we reestablish meter at a boundary depth of ``1``

            >>> for staff in score:
            ...     for container in staff:
            ...         leaf = abjad.get.leaf(container, 0)
            ...         time_signature = abjad.get.indicator(
            ...             leaf,
            ...             abjad.TimeSignature
            ...             )
            ...         abjad.Meter.rewrite_meter(
            ...             container[:],
            ...             time_signature,
            ...             boundary_depth=1,
            ...             )
            ...
            >>> abjad.show(score) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                \with
                {
                    \remove Timing_translator
                    \remove Time_signature_engraver
                    \remove Default_bar_line_engraver
                }
                <<
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 3/4
                            c'2
                            c'4
                        }
                        {
                            \time 3/4
                            c'4
                            c'2
                        }
                        {
                            \time 3/4
                            c'4
                            ~
                            c'8
                            c'8
                            ~
                            c'4
                        }
                        {
                            \time 3/4
                            c'2
                            ~
                            c'8
                            c'8
                        }
                        {
                            \time 3/4
                            c'8
                            c'8
                            ~
                            c'2
                        }
                    }
                    \new Staff
                    \with
                    {
                        \consists Timing_translator
                        \consists Time_signature_engraver
                        \consists Default_bar_line_engraver
                    }
                    {
                        {
                            \time 6/8
                            c'4.
                            ~
                            c'8
                            c'4
                        }
                        {
                            \time 6/8
                            c'4
                            c'8
                            ~
                            c'4.
                        }
                        {
                            \time 6/8
                            c'4.
                            c'4.
                        }
                        {
                            \time 6/8
                            c'4.
                            ~
                            c'4
                            c'8
                        }
                        {
                            \time 6/8
                            c'8
                            c'4
                            ~
                            c'4.
                        }
                    }
                >>

            Note that the two time signatures are much more clearly
            disambiguated above.

        ..  container:: example

            Establishing meter recursively in measures with nested tuplets:

            >>> lily_string = "| 4/4 c'16 ~ c'4 d'8. ~ "
            >>> lily_string += "2/3 { d'8. ~ 3/5 { d'16 e'8. f'16 ~ } } "
            >>> lily_string += "f'4 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 4/4
                        c'16
                        ~
                        c'4
                        d'8.
                        ~
                        \times 2/3 {
                            d'8.
                            ~
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 3/5 {
                                d'16
                                e'8.
                                f'16
                                ~
                            }
                        }
                        f'4
                    }
                }

            When establishing a meter on a selection of components which
            contain containers, like tuplets or containers, ``rewrite_meter()``
            will recurse into those containers, treating them as measures whose
            time signature is derived from the preprolated preprolated_duration
            of the container's contents:

            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(
            ...     measure[0],
            ...     abjad.TimeSignature
            ...     )
            >>> abjad.Meter.rewrite_meter(
            ...     measure[:],
            ...     time_signature,
            ...     boundary_depth=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    {
                        \time 4/4
                        c'4
                        ~
                        c'16
                        d'8.
                        ~
                        \times 2/3 {
                            d'8
                            ~
                            d'16
                            ~
                            \tweak text #tuplet-number::calc-fraction-text
                            \times 3/5 {
                                d'16
                                e'8
                                ~
                                e'16
                                f'16
                                ~
                            }
                        }
                        f'4
                    }
                }

        ..  container:: example

            Default rewrite behavior doesn't subdivide the first note in this
            measure because the first note in the measure starts at the
            beginning of a level-0 beat in meter:

            >>> staff = abjad.Staff("c'4.. c'16 ~ c'4")
            >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
            >>> meter = abjad.Meter((6, 8))
            >>> abjad.Meter.rewrite_meter(staff[:], meter)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 6/8
                    c'4..
                    c'16
                    ~
                    c'4
                }

            Setting boundary depth to 1 subdivides the first note in this
            measure:

            >>> staff = abjad.Staff("c'4.. c'16 ~ c'4")
            >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
            >>> meter = abjad.Meter((6, 8))
            >>> abjad.Meter.rewrite_meter(staff[:], meter, boundary_depth=1)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 6/8
                    c'4.
                    ~
                    c'16
                    c'16
                    ~
                    c'4
                }

            Another way of doing this is by setting preferred boundary depth on
            the meter itself:

            >>> staff = abjad.Staff("c'4.. c'16 ~ c'4")
            >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
            >>> meter = abjad.Meter(
            ...     (6, 8),
            ...     preferred_boundary_depth=1,
            ...     )
            >>> abjad.Meter.rewrite_meter(staff[:], meter)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 6/8
                    c'4.
                    ~
                    c'16
                    c'16
                    ~
                    c'4
                }

            This makes it possible to divide different meters in different
            ways.

        ..  container:: example

            Rewrites notes and tuplets:

            >>> lily_string = r"c'8 ~ c'8 ~ c'8 \times 6/7 { c'4. r16 }"
            >>> lily_string += r" \times 6/7 { r16 c'4. } c'8 ~ c'8 ~ c'8"
            >>> staff = abjad.Staff(lily_string)
            >>> abjad.attach(abjad.TimeSignature((6, 4)), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 6/4
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'4.
                    }
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                }

            >>> meter = abjad.Meter((6, 4))
            >>> abjad.Meter.rewrite_meter(
            ...     staff[:],
            ...     meter,
            ...     boundary_depth=1,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 6/4
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'8.
                        ~
                        c'8
                        ~
                        c'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'8
                        ~
                        c'4
                    }
                    c'4.
                }

            The tied note rewriting is good while the tuplet rewriting
            could use some adjustment.

            Rewrites notes but not tuplets:

            >>> lily_string = r"c'8 ~ c'8 ~ c'8 \times 6/7 { c'4. r16 }"
            >>> lily_string += r" \times 6/7 { r16 c'4. } c'8 ~ c'8 ~ c'8"
            >>> staff = abjad.Staff(lily_string)
            >>> abjad.attach(abjad.TimeSignature((6, 4)), staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 6/4
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'4.
                    }
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                }

            >>> meter = abjad.Meter((6, 4))
            >>> abjad.Meter.rewrite_meter(
            ...     staff[:],
            ...     meter,
            ...     boundary_depth=1,
            ...     rewrite_tuplets=False,
            ...     )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 6/4
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \times 6/7 {
                        r16
                        c'4.
                    }
                    c'4.
                }

        Operates in place and returns none.
        """

        def recurse(
            boundary_depth=None,
            boundary_offsets=None,
            depth=0,
            logical_tie=None,
        ):
            offsets = _MeterManager.get_offsets_at_depth(depth, offset_inventory)
            logical_tie_duration = logical_tie._get_preprolated_duration()
            logical_tie_timespan = _inspect._get_timespan(logical_tie)
            logical_tie_start_offset = logical_tie_timespan.start_offset
            logical_tie_stop_offset = logical_tie_timespan.stop_offset
            logical_tie_starts_in_offsets = logical_tie_start_offset in offsets
            logical_tie_stops_in_offsets = logical_tie_stop_offset in offsets
            if not _MeterManager.is_acceptable_logical_tie(
                logical_tie_duration=logical_tie_duration,
                logical_tie_starts_in_offsets=logical_tie_starts_in_offsets,
                logical_tie_stops_in_offsets=logical_tie_stops_in_offsets,
                maximum_dot_count=maximum_dot_count,
            ):
                split_offset = None
                offsets = _MeterManager.get_offsets_at_depth(depth, offset_inventory)
                # If the logical tie's start aligns,
                # take the latest possible offset.
                if logical_tie_starts_in_offsets:
                    offsets = reversed(offsets)
                for offset in offsets:
                    if logical_tie_start_offset < offset < logical_tie_stop_offset:
                        split_offset = offset
                        break
                if split_offset is not None:
                    split_offset -= logical_tie_start_offset
                    shards = mutate.split(logical_tie[:], [split_offset])
                    logical_ties = [LogicalTie(_) for _ in shards]
                    for logical_tie in logical_ties:
                        recurse(
                            boundary_depth=boundary_depth,
                            boundary_offsets=boundary_offsets,
                            depth=depth,
                            logical_tie=logical_tie,
                        )
                else:
                    recurse(
                        boundary_depth=boundary_depth,
                        boundary_offsets=boundary_offsets,
                        depth=depth + 1,
                        logical_tie=logical_tie,
                    )
            elif _MeterManager.is_boundary_crossing_logical_tie(
                boundary_depth=boundary_depth,
                boundary_offsets=boundary_offsets,
                logical_tie_start_offset=logical_tie_start_offset,
                logical_tie_stop_offset=logical_tie_stop_offset,
            ):
                offsets = boundary_offsets
                if logical_tie_start_offset in boundary_offsets:
                    offsets = reversed(boundary_offsets)
                split_offset = None
                for offset in offsets:
                    if logical_tie_start_offset < offset < logical_tie_stop_offset:
                        split_offset = offset
                        break
                assert split_offset is not None
                split_offset -= logical_tie_start_offset
                shards = mutate.split(logical_tie[:], [split_offset])
                logical_ties = [LogicalTie(shard) for shard in shards]
                for logical_tie in logical_ties:
                    recurse(
                        boundary_depth=boundary_depth,
                        boundary_offsets=boundary_offsets,
                        depth=depth,
                        logical_tie=logical_tie,
                    )
            else:
                mutate._fuse(logical_tie[:])

        assert isinstance(components, Selection), repr(components)
        if not isinstance(meter, Meter):
            meter = Meter(meter)
        boundary_depth = boundary_depth or meter.preferred_boundary_depth
        # Validate arguments.
        assert Selection(components).are_contiguous_logical_voice(
            ignore_before_after_grace=True
        )
        if not isinstance(meter, Meter):
            meter = Meter(meter)
        if boundary_depth is not None:
            boundary_depth = int(boundary_depth)
        if maximum_dot_count is not None:
            maximum_dot_count = int(maximum_dot_count)
            assert 0 <= maximum_dot_count
        if initial_offset is None:
            initial_offset = Offset(0)
        initial_offset = Offset(initial_offset)
        first_start_offset = components[0]._get_timespan().start_offset
        last_start_offset = components[-1]._get_timespan().start_offset
        difference = last_start_offset - first_start_offset + initial_offset
        assert difference < meter.implied_time_signature.duration
        # Build offset inventory, adjusted for initial offset and prolation.
        first_offset = components[0]._get_timespan().start_offset
        first_offset -= initial_offset
        if components[0]._parent is None:
            prolation = 1
        else:
            parentage = Parentage(components[0]._parent)
            prolation = parentage.prolation
        offset_inventory = []
        for offsets in meter.depthwise_offset_inventory:
            offsets = [(_ * prolation) + first_offset for _ in offsets]
            offset_inventory.append(tuple(offsets))
        # Build boundary offset inventory, if applicable.
        if boundary_depth is not None:
            boundary_offsets = offset_inventory[boundary_depth]
        else:
            boundary_offsets = None
        # Cache results of iterator;
        # we'll be mutating the underlying collection
        iterator = _MeterManager.iterate_rewrite_inputs(components)
        items = tuple(iterator)
        for item in items:
            if isinstance(item, LogicalTie):
                recurse(
                    boundary_depth=boundary_depth,
                    boundary_offsets=boundary_offsets,
                    depth=0,
                    logical_tie=item,
                )
            elif isinstance(item, Tuplet) and not rewrite_tuplets:
                pass
            else:
                preprolated_duration = sum(
                    [_._get_preprolated_duration() for _ in item]
                )
                if preprolated_duration.numerator == 1:
                    preprolated_duration = NonreducedFraction(preprolated_duration)
                    preprolated_duration = preprolated_duration.with_denominator(
                        preprolated_duration.denominator * 4
                    )
                sub_metrical_hierarchy = Meter(preprolated_duration)
                sub_boundary_depth = 1
                if boundary_depth is None:
                    sub_boundary_depth = None
                Meter.rewrite_meter(
                    item[:],
                    sub_metrical_hierarchy,
                    boundary_depth=sub_boundary_depth,
                    maximum_dot_count=maximum_dot_count,
                )


class MeterList(TypedList):
    """
    Meter list.

    ..  container:: example

        >>> meters = abjad.MeterList([
        ...     (3, 4), (5, 16), (7, 8),
        ...     ])

        >>> string = abjad.storage(meters)
        >>> print(string)
        abjad.MeterList(
            [
                abjad.Meter(
                    '(3/4 (1/4 1/4 1/4))'
                    ),
                abjad.Meter(
                    '(5/16 ((3/16 (1/16 1/16 1/16)) (2/16 (1/16 1/16))))'
                    ),
                abjad.Meter(
                    '(7/8 ((3/8 (1/8 1/8 1/8)) (2/8 (1/8 1/8)) (2/8 (1/8 1/8))))'
                    ),
                ]
            )

        >>> abjad.show(meters, scale=0.5) # doctest: +SKIP

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### SPECIAL METHODS ###

    def __illustrate__(self, denominator=16, range_=None, scale=None) -> LilyPondFile:
        r"""
        Illustrates meters.

        ..  container:: example

            >>> meters = abjad.MeterList([(3, 4), (5, 16), (7, 8)])
            >>> abjad.show(meters, scale=0.5) # doctest: +SKIP

            ..  doctest

                >>> lilypond_file = meters.__illustrate__()
                >>> markup = lilypond_file.items[0]
                >>> string = abjad.lilypond(markup)
                >>> print(string)
                \markup { \column { \combine \combine \translate #'(1.0 . 1) \sans \fontsize #-3 \center-align \fraction 3 4 \translate #'(49.38709677419355 . 1) \sans \fontsize #-3 \center-align \fraction 5 16 \translate #'(69.54838709677419 . 1) \sans \fontsize #-3 \center-align \fraction 7 8 \combine \postscript
                    #"
                    0.2 setlinewidth
                    1 0.5 moveto
                    49.38709677419355 0.5 lineto
                    stroke
                    1 1.25 moveto
                    1 -0.25 lineto
                    stroke
                    49.38709677419355 1.25 moveto
                    49.38709677419355 -0.25 lineto
                    stroke
                    49.38709677419355 0.5 moveto
                    69.54838709677419 0.5 lineto
                    stroke
                    49.38709677419355 1.25 moveto
                    49.38709677419355 -0.25 lineto
                    stroke
                    69.54838709677419 1.25 moveto
                    69.54838709677419 -0.25 lineto
                    stroke
                    69.54838709677419 0.5 moveto
                    126 0.5 lineto
                    stroke
                    69.54838709677419 1.25 moveto
                    69.54838709677419 -0.25 lineto
                    stroke
                    126 1.25 moveto
                    126 -0.25 lineto
                    stroke
                    " \postscript #"1 -2 moveto
                0 -6.153846153846154 rlineto
                stroke
                5.032258064516129 -2 moveto
                0 -1.5384615384615385 rlineto
                stroke
                9.064516129032258 -2 moveto
                0 -3.076923076923077 rlineto
                stroke
                13.096774193548388 -2 moveto
                0 -1.5384615384615385 rlineto
                stroke
                17.129032258064516 -2 moveto
                0 -4.615384615384616 rlineto
                stroke
                21.161290322580644 -2 moveto
                0 -1.5384615384615385 rlineto
                stroke
                25.193548387096776 -2 moveto
                0 -3.076923076923077 rlineto
                stroke
                29.225806451612904 -2 moveto
                0 -1.5384615384615385 rlineto
                stroke
                33.25806451612903 -2 moveto
                0 -4.615384615384616 rlineto
                stroke
                37.29032258064516 -2 moveto
                0 -1.5384615384615385 rlineto
                stroke
                41.32258064516129 -2 moveto
                0 -3.076923076923077 rlineto
                stroke
                45.354838709677416 -2 moveto
                0 -1.5384615384615385 rlineto
                stroke
                49.38709677419355 -2 moveto
                0 -6.153846153846154 rlineto
                stroke
                49.38709677419355 -2 moveto
                0 -10.909090909090908 rlineto
                stroke
                53.41935483870968 -2 moveto
                0 -3.6363636363636367 rlineto
                stroke
                57.45161290322581 -2 moveto
                0 -3.6363636363636367 rlineto
                stroke
                61.483870967741936 -2 moveto
                0 -7.272727272727273 rlineto
                stroke
                65.51612903225806 -2 moveto
                0 -3.6363636363636367 rlineto
                stroke
                69.54838709677419 -2 moveto
                0 -10.909090909090908 rlineto
                stroke
                69.54838709677419 -2 moveto
                0 -5.517241379310345 rlineto
                stroke
                73.58064516129032 -2 moveto
                0 -1.3793103448275863 rlineto
                stroke
                77.61290322580645 -2 moveto
                0 -2.7586206896551726 rlineto
                stroke
                81.64516129032258 -2 moveto
                0 -1.3793103448275863 rlineto
                stroke
                85.6774193548387 -2 moveto
                0 -2.7586206896551726 rlineto
                stroke
                89.70967741935483 -2 moveto
                0 -1.3793103448275863 rlineto
                stroke
                93.74193548387096 -2 moveto
                0 -4.137931034482759 rlineto
                stroke
                97.7741935483871 -2 moveto
                0 -1.3793103448275863 rlineto
                stroke
                101.80645161290323 -2 moveto
                0 -2.7586206896551726 rlineto
                stroke
                105.83870967741936 -2 moveto
                0 -1.3793103448275863 rlineto
                stroke
                109.87096774193549 -2 moveto
                0 -4.137931034482759 rlineto
                stroke
                113.90322580645162 -2 moveto
                0 -1.3793103448275863 rlineto
                stroke
                117.93548387096774 -2 moveto
                0 -2.7586206896551726 rlineto
                stroke
                121.96774193548387 -2 moveto
                0 -1.3793103448275863 rlineto
                stroke
                126 -2 moveto
                0 -5.517241379310345 rlineto
                stroke" } }

        Returns LilyPond file.
        """
        durations = [_.duration for _ in self]
        total_duration = sum(durations)
        offsets = math.cumulative_sums(durations, start=0)
        timespans = TimespanList()
        for one, two in Sequence(offsets).nwise():
            timespan = Timespan(start_offset=one, stop_offset=two)
            timespans.append(timespan)
        if range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = 0, total_duration
        minimum = float(Offset(minimum))
        maximum = float(Offset(maximum))
        if scale is None:
            scale = 1.0
        assert 0 < scale
        postscript_scale = 125.0 / (maximum - minimum)
        postscript_scale *= float(scale)
        postscript_x_offset = (minimum * postscript_scale) - 1
        timespan_markup = timespans._make_timespan_list_markup(
            timespans,
            postscript_x_offset,
            postscript_scale,
            draw_offsets=False,
        )
        timespan_string = timespan_markup.contents[0]
        ps = markups.Postscript()
        rational_x_offset = Offset(0)
        for meter in self:
            kernel_denominator = denominator or meter.denominator
            kernel = MetricAccentKernel.from_meter(meter, kernel_denominator)
            for offset, weight in sorted(kernel.kernel.items()):
                weight = float(weight) * -40
                ps_x_offset = float(rational_x_offset + offset)
                ps_x_offset *= postscript_scale
                ps_x_offset += 1
                ps = ps.moveto(ps_x_offset, -2)
                ps = ps.rlineto(0, weight)
                ps = ps.stroke()
            rational_x_offset += meter.duration
        ps_markup = rf'\postscript #"{ps}"'
        lines_string = rf"\combine {timespan_string} {ps_markup}"
        fraction_markups = []
        for meter, offset in zip(self, offsets):
            numerator, denominator = meter.numerator, meter.denominator
            x_translation = float(offset) * postscript_scale
            x_translation -= postscript_x_offset
            string = rf"\translate #'({x_translation} . 1) \sans \fontsize #-3"
            string += rf" \center-align \fraction {numerator} {denominator}"
            fraction = markups.Markup(string, literal=True)
            fraction_markups.append(fraction)
        fraction_markup = str(fraction_markups[0].contents[0])
        for markup in fraction_markups[1:]:
            fraction_markup = rf"\combine {fraction_markup} {markup.contents[0]}"
        string = rf"\markup {{ \column {{ {fraction_markup} {lines_string} }} }}"
        markup = markups.Markup(string, literal=True)
        lilypond_file = LilyPondFile()
        markup = new(markup, direction=None)
        lilypond_file.items.append(markup)
        return lilypond_file

    ### PRIVATE METHODS ###

    def _coerce_item(self, item):
        return Meter(item)


class MetricAccentKernel:
    """
    Metric accent kernel.

    ..  container:: example

        >>> hierarchy = abjad.Meter((7, 8))
        >>> kernel = hierarchy.generate_offset_kernel_to_denominator(8)
        >>> kernel
        MetricAccentKernel(
            {
                Offset((0, 1)): Multiplier(3, 14),
                Offset((1, 8)): Multiplier(1, 14),
                Offset((1, 4)): Multiplier(1, 14),
                Offset((3, 8)): Multiplier(1, 7),
                Offset((1, 2)): Multiplier(1, 14),
                Offset((5, 8)): Multiplier(1, 7),
                Offset((3, 4)): Multiplier(1, 14),
                Offset((7, 8)): Multiplier(3, 14),
                }
            )

    Call the kernel against an expression from which offsets can be counted
    to receive an impulse-response:

    ..  container:: example

        >>> offsets = [(0, 8), (1, 8), (1, 8), (3, 8)]
        >>> kernel(offsets)
        Multiplier(1, 2)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_kernel", "_offsets")

    ### INITIALIZER ###

    def __init__(self, kernel=None):
        kernel = kernel or {}
        assert isinstance(kernel, dict)
        for key, value in kernel.items():
            assert isinstance(key, Offset)
            assert isinstance(value, Multiplier)
        self._kernel = kernel.copy()
        self._offsets = tuple(sorted(self._kernel))

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        r"""
        Calls metrical accent kernal on ``argument``.

        >>> upper_staff = abjad.Staff("c'8 d'4. e'8 f'4.")
        >>> lower_staff = abjad.Staff(r'\clef bass c4 b,4 a,2')
        >>> score = abjad.Score([upper_staff, lower_staff])

        >>> kernel = abjad.MetricAccentKernel.from_meter((4, 4))
        >>> kernel(score)
        Multiplier(10, 33)

        Returns float.
        """
        offset_count = self.count_offsets(argument)
        response = Multiplier(0, 1)
        for offset, count in offset_count.items():
            if offset in self._kernel:
                weight = self._kernel[offset]
                weighted_count = weight * count
                response += weighted_count
        return response

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a metrical accent kernal with a kernal
        equal to that of this metrical accent kernel.

        Returns true or false.
        """
        return super().__eq__(argument)

    def __hash__(self):
        """
        Hashes metric accent kernel.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            repr_is_indented=True,
            storage_format_args_values=[self.kernel],
            storage_format_keyword_names=[],
        )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        """
        Gets duration.
        """
        return Duration(self._offsets[-1])

    @property
    def kernel(self):
        """
        The kernel datastructure.

        Returns dict.
        """
        return self._kernel.copy()

    ### PUBLIC METHODS ###

    @staticmethod
    def count_offsets(argument) -> OffsetCounter:
        r"""
        Count offsets in ``argument``.

        ..  container:: example

            >>> upper_staff = abjad.Staff("c'8 d'4. e'8 f'4.")
            >>> lower_staff = abjad.Staff(r'\clef bass c4 b,4 a,2')
            >>> score = abjad.Score([upper_staff, lower_staff])

            ..  docs::

                >>> string = abjad.lilypond(score)
                >>> print(string)
                \new Score
                <<
                    \new Staff
                    {
                        c'8
                        d'4.
                        e'8
                        f'4.
                    }
                    \new Staff
                    {
                        \clef "bass"
                        c4
                        b,4
                        a,2
                    }
                >>

            >>> abjad.show(score) # doctest: +SKIP

            >>> MetricAccentKernel = abjad.MetricAccentKernel
            >>> leaves = abjad.select(score).leaves()
            >>> counter = abjad.MetricAccentKernel.count_offsets(leaves)
            >>> for offset, count in sorted(counter.items()):
            ...     offset, count
            (Offset((0, 1)), 2)
            (Offset((1, 8)), 2)
            (Offset((1, 4)), 2)
            (Offset((1, 2)), 4)
            (Offset((5, 8)), 2)
            (Offset((1, 1)), 2)

        ..  container:: example

            >>> a = abjad.Timespan(0, 10)
            >>> b = abjad.Timespan(5, 15)
            >>> c = abjad.Timespan(15, 20)

            >>> counter = MetricAccentKernel.count_offsets((a, b, c))
            >>> for offset, count in sorted(counter.items()):
            ...     offset, count
            (Offset((0, 1)), 1)
            (Offset((5, 1)), 1)
            (Offset((10, 1)), 1)
            (Offset((15, 1)), 2)
            (Offset((20, 1)), 1)

        Returns counter.
        """
        return OffsetCounter(argument)

    @staticmethod
    def from_meter(meter, denominator=32, normalize=True):
        """
        Create a metric accent kernel from ``meter``.

        Returns new metric accent kernel.
        """
        if not isinstance(meter, Meter):
            meter = Meter(meter)
        return meter.generate_offset_kernel_to_denominator(
            denominator=denominator, normalize=normalize
        )


class _MeterFittingSession:
    """
    Meter-fitting session.

    Used internally by Meter.fit_meters().
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_cached_offset_counters",
        "_kernel_denominator",
        "_kernels",
        "_longest_kernel",
        "_maximum_run_length",
        "_meters",
        "_offset_counter",
        "_ordered_offsets",
    )

    KernelScore = collections.namedtuple("KernelScore", ("kernel", "score"))

    ### INITIALIZER ###

    def __init__(
        self,
        kernel_denominator=32,
        maximum_run_length=None,
        meters=None,
        offset_counter=None,
    ):
        self._cached_offset_counters = {}
        if maximum_run_length is not None:
            maximum_run_length = int(maximum_run_length)
            assert 0 < maximum_run_length
        self._maximum_run_length = maximum_run_length
        if offset_counter:
            self._offset_counter = MetricAccentKernel.count_offsets(offset_counter)
        else:
            self._offset_counter = {}
        self._ordered_offsets = tuple(sorted(self.offset_counter))
        meters = meters or ()
        self._meters = tuple(Meter(_) for _ in meters)
        self._kernel_denominator = Duration(kernel_denominator)
        self._kernels = {}
        for meter in self._meters:
            kernel = meter.generate_offset_kernel_to_denominator(
                self._kernel_denominator
            )
            self._kernels[kernel] = meter
        if self.kernels:
            self._longest_kernel = sorted(self._kernels, key=lambda _: _.duration)[-1]
        else:
            self._longest_kernel = None

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Fits meters.

        Returns meter list.
        """
        selected_kernels = []
        current_offset = Offset(0)
        while current_offset < self.ordered_offsets[-1]:
            kernel_scores = []
            kernels = self._get_kernels(selected_kernels)
            offset_counter = self._get_offset_counter_at(current_offset)
            if not offset_counter:
                winning_kernel = self.longest_kernel
                if selected_kernels:
                    winning_kernel = selected_kernels[-1]
            else:
                for kernel in kernels:
                    if (
                        self.maximum_run_length
                        and 1 < len(kernels)
                        and self.maximum_run_length <= len(selected_kernels)
                    ):
                        last_n_kernels = selected_kernels[-self.maximum_run_length :]
                        if len(set(last_n_kernels)) == 1:
                            if kernel == last_n_kernels[-1]:
                                continue
                    initial_score = kernel(offset_counter)
                    lookahead_score = self._get_lookahead_score(
                        current_offset, kernel, kernels
                    )
                    score = initial_score + lookahead_score
                    kernel_score = self.KernelScore(kernel=kernel, score=score)
                    kernel_scores.append(kernel_score)
                kernel_scores.sort(key=lambda kernel_score: kernel_score.score)
                winning_kernel = kernel_scores[-1].kernel
            selected_kernels.append(winning_kernel)
            current_offset += winning_kernel.duration
        selected_meters = (self.kernels[_] for _ in selected_kernels)
        selected_meters = MeterList(selected_meters)
        return selected_meters

    ### PRIVATE METHODS ###

    def _get_kernels(self, selected_kernels):
        return tuple(self.kernels)

    def _get_lookahead_score(self, current_offset, kernel, kernels):
        lookahead_scores = []
        lookahead_offset = current_offset + kernel.duration
        lookahead_offset_counter = self._get_offset_counter_at(lookahead_offset)
        for lookahead_kernel in kernels:
            lookahead_scores.append(lookahead_kernel(lookahead_offset_counter))
        lookahead_score = sum(lookahead_scores)  # / len(lookahead_scores)
        return lookahead_score

    def _get_offset_counter_at(self, start_offset):
        if start_offset in self.cached_offset_counters:
            return self.cached_offset_counters[start_offset]
        offset_counter = {}
        stop_offset = start_offset + self.longest_kernel.duration
        index = bisect.bisect_left(self.ordered_offsets, start_offset)
        if index == len(self.ordered_offsets):
            return offset_counter
        offset = self.ordered_offsets[index]
        while offset <= stop_offset:
            count = self.offset_counter[offset]
            offset_counter[offset - start_offset] = count
            index += 1
            if index == len(self.ordered_offsets):
                break
            offset = self.ordered_offsets[index]
        self.cached_offset_counters[start_offset] = offset_counter
        return offset_counter

    ### PUBLIC PROPERTIES ###

    @property
    def cached_offset_counters(self):
        """
        Gets cached offset counters

        Returns dictionary.
        """
        return self._cached_offset_counters

    @property
    def kernel_denominator(self):
        """
        Gets kernel denominator.

        Returns duration.
        """
        return self._kernel_denominator

    @property
    def kernels(self):
        """
        Gets kernels-to-meter dictionary.

        Returns dictionary.
        """
        return self._kernels

    @property
    def longest_kernel(self):
        """
        Gets longest kernel.

        Returns kernel.
        """
        return self._longest_kernel

    @property
    def maximum_run_length(self):
        """
        Gets maximum meter repetitions.

        Returns integer or none.
        """
        return self._maximum_run_length

    @property
    def meters(self):
        """
        Gets meters.

        Returns meters.
        """
        return self._meters

    @property
    def offset_counter(self):
        """
        Gets offset counter.

        Returns offset counter.
        """
        return self._offset_counter

    @property
    def ordered_offsets(self):
        """
        Gets ordered offsets.

        Returns offsets.
        """
        return self._ordered_offsets


class _MeterManager:
    """
    Meter manager.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### PUBLIC METHODS ###

    @staticmethod
    def get_offsets_at_depth(depth, offset_inventory):
        """
        Gets offsets at ``depth`` in ``offset_inventory``.
        """
        if depth < len(offset_inventory):
            return offset_inventory[depth]
        while len(offset_inventory) <= depth:
            new_offsets = []
            old_offsets = offset_inventory[-1]
            for first, second in Sequence(old_offsets).nwise():
                new_offsets.append(first)
                difference = second - first
                half = (first + second) / 2
                if Duration(1, 8) < difference:
                    new_offsets.append(half)
                else:
                    one_quarter = (first + half) / 2
                    three_quarters = (half + second) / 2
                    new_offsets.append(one_quarter)
                    new_offsets.append(half)
                    new_offsets.append(three_quarters)
            new_offsets.append(old_offsets[-1])
            offset_inventory.append(tuple(new_offsets))
        return offset_inventory[depth]

    @staticmethod
    def is_acceptable_logical_tie(
        logical_tie_duration=None,
        logical_tie_starts_in_offsets=None,
        logical_tie_stops_in_offsets=None,
        maximum_dot_count=None,
    ):
        """
        Is true if logical tie is acceptable.
        """
        # print '\tTESTING ACCEPTABILITY'
        if not logical_tie_duration.is_assignable:
            return False
        if (
            maximum_dot_count is not None
            and maximum_dot_count < logical_tie_duration.dot_count
        ):
            return False
        if not logical_tie_starts_in_offsets and not logical_tie_stops_in_offsets:
            return False
        return True

    @staticmethod
    def is_boundary_crossing_logical_tie(
        boundary_depth=None,
        boundary_offsets=None,
        logical_tie_start_offset=None,
        logical_tie_stop_offset=None,
    ):
        """
        Is true if logical tie crosses meter boundaries.
        """
        # print '\tTESTING BOUNDARY CROSSINGS'
        if boundary_depth is None:
            return False
        if not any(
            logical_tie_start_offset < _ < logical_tie_stop_offset
            for _ in boundary_offsets
        ):
            return False
        if (
            logical_tie_start_offset in boundary_offsets
            and logical_tie_stop_offset in boundary_offsets
        ):
            return False
        return True

    @staticmethod
    def iterate_rewrite_inputs(argument):
        r"""
        Iterates topmost masked logical ties, rest groups and containers
        in ``argument``, masked by ``argument``.

        >>> string = "! 2/4 c'4 d'4 ~ !"
        >>> string += "! 4/4 d'8. r16 r8. e'16 ~ "
        >>> string += "2/3 { e'8 ~ e'8 f'8 ~ } f'4 ~ !"
        >>> string += "! 4/4 f'8 g'8 ~ g'4 a'4 ~ a'8 b'8 ~ !"
        >>> string += "! 2/4 b'4 c''4 !"
        >>> string = string.replace('!', '|')
        >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(string)
        >>> staff = abjad.Staff()
        >>> staff[:] = container

        ..  docs::

            >>> string = abjad.lilypond(staff)
            >>> print(string)
            \new Staff
            {
                {
                    \time 2/4
                    c'4
                    d'4
                    ~
                }
                {
                    \time 4/4
                    d'8.
                    r16
                    r8.
                    e'16
                    ~
                    \times 2/3 {
                        e'8
                        ~
                        e'8
                        f'8
                        ~
                    }
                    f'4
                    ~
                }
                {
                    \time 4/4
                    f'8
                    g'8
                    ~
                    g'4
                    a'4
                    ~
                    a'8
                    b'8
                    ~
                }
                {
                    \time 2/4
                    b'4
                    c''4
                }
            }

        >>> for x in abjad.meter._MeterManager.iterate_rewrite_inputs(
        ...     staff[0]): x
        ...
        LogicalTie([Note("c'4")])
        LogicalTie([Note("d'4")])

        >>> for x in abjad.meter._MeterManager.iterate_rewrite_inputs(
        ...     staff[1]): x
        ...
        LogicalTie([Note("d'8.")])
        LogicalTie([Rest('r16'), Rest('r8.')])
        LogicalTie([Note("e'16")])
        Tuplet('3:2', "e'8 e'8 f'8")
        LogicalTie([Note("f'4")])

        >>> for x in abjad.meter._MeterManager.iterate_rewrite_inputs(
        ...     staff[2]): x
        ...
        LogicalTie([Note("f'8")])
        LogicalTie([Note("g'8"), Note("g'4")])
        LogicalTie([Note("a'4"), Note("a'8")])
        LogicalTie([Note("b'8")])

        >>> for x in abjad.meter._MeterManager.iterate_rewrite_inputs(
        ...     staff[3]): x
        ...
        LogicalTie([Note("b'4")])
        LogicalTie([Note("c''4")])

        Returns generator.
        """
        last_tie = None
        current_leaf_group = None
        current_leaf_group_is_silent = False
        for component in argument:
            if isinstance(component, (Note, Chord)):
                this_tie_leaves = _iterate._get_logical_tie_leaves(component)
                this_tie = LogicalTie(this_tie_leaves)
                if current_leaf_group is None:
                    current_leaf_group = []
                elif (
                    current_leaf_group_is_silent
                    or this_tie is None
                    or last_tie != this_tie
                ):
                    yield LogicalTie(current_leaf_group)
                    current_leaf_group = []
                current_leaf_group_is_silent = False
                current_leaf_group.append(component)
                last_tie = this_tie
            elif isinstance(component, (Rest, Skip)):
                if current_leaf_group is None:
                    current_leaf_group = []
                elif not current_leaf_group_is_silent:
                    yield LogicalTie(current_leaf_group)
                    current_leaf_group = []
                current_leaf_group_is_silent = True
                current_leaf_group.append(component)
                last_tie = None
            elif isinstance(component, Container):
                if current_leaf_group is not None:
                    yield LogicalTie(current_leaf_group)
                    current_leaf_group = None
                    last_tie = None
                yield component
            else:
                raise Exception(f"unhandled component: {component!r}.")
        if current_leaf_group is not None:
            yield LogicalTie(current_leaf_group)
