"""
Tools for modeling musical meter.
"""

import bisect
import collections
import fractions
import typing

import uqbar.graphs

from . import _getlib, _iterlib
from . import duration as _duration
from . import indicators as _indicators
from . import lilypondfile as _lilypondfile
from . import math as _math
from . import mutate as _mutate
from . import parentage as _parentage
from . import rhythmtrees as _rhythmtrees
from . import score as _score
from . import select as _select
from . import sequence as _sequence
from . import timespan as _timespan


class Meter:
    """
    Meter.

    Meter models rhythmic organization structured as a tree.

    ..  container:: example

        ``4/4`` grouped two different ways:

        >>> rtc = abjad.meter.make_best_guess_rtc((4, 4))
        >>> meter = abjad.Meter(rtc)
        >>> print(meter.pretty_rtm_format)
        (4/4 (
            1/4
            1/4
            1/4
            1/4))

        >>> abjad.graph(meter) # doctest: +SKIP

        >>> string = "(4/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4))))"
        >>> rtc = abjad.rhythmtrees.parse(string)[0]
        >>> meter = abjad.Meter(rtc)
        >>> print(meter.pretty_rtm_format)
        (4/4 (
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

        >>> abjad.graph(meter) # doctest: +SKIP

    ..  container:: example

        ``6/4`` grouped four different ways:

        >>> rtc = abjad.meter.make_best_guess_rtc((6, 4))
        >>> meter = abjad.Meter(rtc)
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

        >>> string = "(6/4 (1/4 1/4 1/4 1/4 1/4 1/4))"
        >>> rtc = abjad.rhythmtrees.parse(string)[0]
        >>> meter = abjad.Meter(rtc)
        >>> print(meter.pretty_rtm_format)
        (6/4 (
            1/4
            1/4
            1/4
            1/4
            1/4
            1/4))

        >>> abjad.graph(meter) # doctest: +SKIP

        >>> string = "(6/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))"
        >>> rtc = abjad.rhythmtrees.parse(string)[0]
        >>> meter = abjad.Meter(rtc)
        >>> print(meter.pretty_rtm_format)
        (6/4 (
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

        >>> abjad.graph(meter) # doctest: +SKIP

        >>> part = "(3/8 (1/8 1/8 1/8))"
        >>> string = f"(6/4 ({part} {part} {part} {part}))"
        >>> rtc = abjad.rhythmtrees.parse(string)[0]
        >>> meter = abjad.Meter(rtc)
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

    ..  container:: example

        ``7/4`` grouped three different ways:

        >>> string = "(7/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4)) (3/4 (1/4 1/4 1/4))))"
        >>> rtc = abjad.rhythmtrees.parse(string)[0]
        >>> meter = abjad.Meter(rtc)
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

        >>> string = "(7/4 ((2/4 (1/4 1/4)) (3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))"
        >>> rtc = abjad.rhythmtrees.parse(string)[0]
        >>> meter = abjad.Meter(rtc)
        >>> print(meter.pretty_rtm_format)
        (7/4 (
            (2/4 (
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

        >>> abjad.graph(meter) # doctest: +SKIP

        >>> string = "(7/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))"
        >>> rtc = abjad.rhythmtrees.parse(string)[0]
        >>> meter = abjad.Meter(rtc)
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

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        "_denominator",
        "_numerator",
        "_root_node",
    )

    ### INITIALIZER ###

    def __init__(
        self,
        root_node: _rhythmtrees.RhythmTreeContainer,
    ) -> None:
        assert isinstance(root_node, _rhythmtrees.RhythmTreeContainer), repr(root_node)
        for node in [root_node] + list(root_node.depth_first()):
            assert node.prolation == 1, (repr(node), repr(node.prolation))
        numerator, denominator = root_node.pair
        self._denominator = denominator
        self._numerator = numerator
        self._root_node = root_node

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Compares ``root_node.rtm_format`` of self to that of ``argument``.
        """
        if isinstance(argument, type(self)):
            return self.root_node.rtm_format == argument.root_node.rtm_format
        return False

    def __graph__(self, **keywords) -> uqbar.graphs.Graph:
        """
        Gets Graphviz format of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((7, 4))
            >>> meter = abjad.Meter(rtc)
            >>> abjad.graph(meter) # doctest: +SKIP

            ..  docs::

                >>> graph = meter.__graph__()
                >>> string = format(graph, 'graphviz')
                >>> print(string)
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

        """

        def make_offset_node(offset, leaf_one=None, leaf_two=None, is_last=False):
            assert isinstance(offset, _duration.Offset), repr(offset)
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
            weight_field = uqbar.graphs.RecordField(
                label="+" * offset_counter.items[offset]
            )
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

        offsets = _sequence.flatten(self.depthwise_offset_inventory, depth=-1)
        offset_counter = _timespan.OffsetCounter(offsets)
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
        root_node = self._root_node
        nodes = [root_node] + list(root_node.depth_first())
        leaves = [_ for _ in nodes if not hasattr(_, "children")]
        for node in nodes:
            graphviz_node = uqbar.graphs.Node()
            graphviz_node.attributes["label"] = node._get_fraction_string()
            if isinstance(node, _rhythmtrees.RhythmTreeContainer):
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
        for one, two in _sequence.nwise(leaves):
            offset = one.stop_offset
            make_offset_node(offset, one, two)
        offset = leaves[-1].stop_offset
        make_offset_node(offset, leaves[-1], is_last=True)
        return graph

    def __hash__(self) -> int:
        """
        Hashes meter.
        """
        return super().__hash__()

    def __iter__(self) -> typing.Iterator[tuple[tuple[int, int], tuple[int, int]]]:
        """
        Iterates meter.

        ..  container:: example

            Iterates ``5/4``:

            >>> rtc = abjad.meter.make_best_guess_rtc((5, 4))
            >>> meter = abjad.Meter(rtc)
            >>> for pair in meter:
            ...    pair
            ...
            ((0, 4), (1, 4))
            ((1, 4), (2, 4))
            ((2, 4), (3, 4))
            ((0, 4), (3, 4))
            ((3, 4), (4, 4))
            ((4, 4), (5, 4))
            ((3, 4), (5, 4))
            ((0, 4), (5, 4))

        """

        def recurse(node):
            nodes = []
            for child in node:
                if isinstance(child, _rhythmtrees.RhythmTreeLeaf):
                    nodes.append(child)
                else:
                    assert isinstance(child, _rhythmtrees.RhythmTreeContainer)
                    nodes.extend(recurse(child))
            nodes.append(node)
            return nodes

        nodes = recurse(self.root_node)
        assert isinstance(nodes, list)
        for node in nodes:
            pair = _duration.with_denominator(node.start_offset, self.denominator)
            start_offset = pair
            pair = _duration.with_denominator(node.stop_offset, self.denominator)
            stop_offset = pair
            yield start_offset, stop_offset

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}({self.rtm_format!r})"

    ### PUBLIC PROPERTIES ###

    @property
    def denominator(self) -> int:
        """
        Gets denominator of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((7, 4))
            >>> meter = abjad.Meter(rtc)
            >>> meter.denominator
            4

        """
        return self._denominator

    @property
    def depthwise_offset_inventory(self) -> tuple:
        """
        Gets depthwise offset inventory of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((7, 4))
            >>> meter = abjad.Meter(rtc)
            >>> for depth, offsets in enumerate(
            ...     meter.depthwise_offset_inventory):
            ...     print(f"{depth}:")
            ...     for offset in offsets:
            ...         print(f"    {offset!r}")
            0:
                Offset((0, 1))
                Offset((7, 4))
            1:
                Offset((0, 1))
                Offset((3, 4))
                Offset((5, 4))
                Offset((7, 4))
            2:
                Offset((0, 1))
                Offset((1, 4))
                Offset((1, 2))
                Offset((3, 4))
                Offset((1, 1))
                Offset((5, 4))
                Offset((3, 2))
                Offset((7, 4))

        """
        inventory = []
        all_offsets = set()
        all_offsets.add(_duration.Offset(self.numerator, self.denominator))
        for depth, nodes in sorted(self.root_node._depthwise_inventory().items()):
            for node in nodes:
                all_offsets.add(_duration.Offset(node.start_offset))
            inventory.append(tuple(sorted(all_offsets)))
        return tuple(inventory)

    @property
    def duration(self) -> _duration.Duration:
        """
        Gets duration of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((7, 4))
            >>> meter = abjad.Meter(rtc)
            >>> meter.duration
            Duration(7, 4)

        """
        return _duration.Duration(self.numerator, self.denominator)

    @property
    def fraction_string(self) -> str:
        """
        Gets fraction string.
        """
        return f"{self.pair[0]}/{self.pair[1]}"

    @property
    def implied_time_signature(self) -> _indicators.TimeSignature:
        """
        Gets implied time signature of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((4, 4))
            >>> meter = abjad.Meter(rtc)
            >>> meter.implied_time_signature
            TimeSignature(pair=(4, 4), hide=False, partial=None)

        """
        pair = self.root_node.pair
        return _indicators.TimeSignature(pair)

    @property
    def is_compound(self) -> bool:
        """
        Is true when meter is compound.

        ..  container:: example

            Compound meters written over ``4``:

            >>> for numerator in range(1, 13):
            ...     rtc = abjad.meter.make_best_guess_rtc((numerator, 4))
            ...     meter = abjad.Meter(rtc)
            ...     string = True if meter.is_compound else ''
            ...     print(str(meter.fraction_string), string)
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
            ...     rtc = abjad.meter.make_best_guess_rtc((numerator, 8))
            ...     meter = abjad.Meter(rtc)
            ...     string = True if meter.is_compound else ''
            ...     print(str(meter.fraction_string), string)
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

        Compound meters defined equal to those meters with a numerator divisible by ``3``
        (but not equal to ``3``).
        """
        if 3 in _math.divisors(self.numerator):
            if not self.numerator == 3:
                return True
        return False

    @property
    def is_simple(self) -> bool:
        """
        Is true when meter is simple.

        ..  container:: example

            Simple meters written over ``4``:

            >>> for numerator in range(1, 13):
            ...     rtc = abjad.meter.make_best_guess_rtc((numerator, 4))
            ...     meter = abjad.Meter(rtc)
            ...     string = True if meter.is_simple else ''
            ...     print(str(meter.fraction_string), string)
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
            ...     rtc = abjad.meter.make_best_guess_rtc((numerator, 8))
            ...     meter = abjad.Meter(rtc)
            ...     string = True if meter.is_simple else ''
            ...     print(str(meter.fraction_string), string)
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

        Simple meters defined equal to those meters with a numerator not divisible by
        ``3``.

        Meters with numerator equal to ``3`` are also defined as simple.
        """
        return not self.is_compound

    @property
    def numerator(self) -> int:
        """
        Gets numerator of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((7, 4))
            >>> meter = abjad.Meter(rtc)
            >>> meter.numerator
            7

        """
        return self._numerator

    @property
    def pair(self) -> tuple[int, int]:
        """
        Gets pair of numerator and denominator of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((6, 4))
            >>> meter = abjad.Meter(rtc)
            >>> meter.pair
            (6, 4)

        """
        return (self.numerator, self.denominator)

    @property
    def pretty_rtm_format(self) -> str:
        """
        Gets pretty RTM format of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((7, 4))
            >>> meter = abjad.Meter(rtc)
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

        """
        return self.root_node.pretty_rtm_format

    @property
    def root_node(self) -> _rhythmtrees.RhythmTreeContainer:
        """
        Gets root node of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((7, 4))
            >>> meter = abjad.Meter(rtc)
            >>> for item in meter.root_node:
            ...     item
            RhythmTreeContainer((3, 4))
            RhythmTreeContainer((2, 4))
            RhythmTreeContainer((2, 4))

        """
        return self._root_node

    @property
    def rtm_format(self) -> str:
        """
        Gets RTM format of meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((7, 4))
            >>> meter = abjad.Meter(rtc)
            >>> meter.rtm_format
            '(7/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'

        """
        return self._root_node.rtm_format

    ### PUBLIC METHODS ###

    @staticmethod
    def fit_meters(
        offset_counter: _timespan.OffsetCounter,
        meters: typing.Sequence["Meter"],
        denominator: int = 32,
        maximum_run_length: int | None = None,
    ) -> list["Meter"]:
        """
        Finds the best-matching sequence of meters for the offsets contained in
        ``offset_counter``.

        ..  container:: example

            >>> pairs = [(3, 4), (4, 4), (5, 4)]
            >>> rtcs = [abjad.meter.make_best_guess_rtc(_) for _ in pairs]
            >>> meters = [abjad.Meter(_) for _ in rtcs]

        ..  container:: example

            Matches a series of hypothetical ``4/4`` measures:

            >>> pairs = [(0, 4), (4, 4), (8, 4), (12, 4), (16, 4)]
            >>> offsets = [abjad.Offset(_) for _ in pairs]
            >>> offset_counter = abjad.OffsetCounter(offsets)
            >>> for meter in abjad.Meter.fit_meters(offset_counter, meters):
            ...     print(meter.implied_time_signature)
            ...
            TimeSignature(pair=(4, 4), hide=False, partial=None)
            TimeSignature(pair=(4, 4), hide=False, partial=None)
            TimeSignature(pair=(4, 4), hide=False, partial=None)
            TimeSignature(pair=(4, 4), hide=False, partial=None)

        ..  container:: example

            Matches a series of hypothetical ``5/4`` measures:

            >>> pairs = [(0, 4), (3, 4), (5, 4), (10, 4), (15, 4), (20, 4)]
            >>> offsets = [abjad.Offset(_) for _ in pairs]
            >>> offset_counter = abjad.OffsetCounter(offsets)
            >>> for meter in abjad.Meter.fit_meters(offset_counter, meters):
            ...     print(meter.implied_time_signature)
            ...
            TimeSignature(pair=(3, 4), hide=False, partial=None)
            TimeSignature(pair=(4, 4), hide=False, partial=None)
            TimeSignature(pair=(3, 4), hide=False, partial=None)
            TimeSignature(pair=(5, 4), hide=False, partial=None)
            TimeSignature(pair=(5, 4), hide=False, partial=None)

        """
        assert all(isinstance(_, Meter) for _ in meters), repr(meters)
        assert isinstance(offset_counter, _timespan.OffsetCounter), repr(offset_counter)
        session = _MeterFittingSession(
            kernel_denominator=denominator,
            maximum_run_length=maximum_run_length,
            meters=meters,
            offset_counter=offset_counter,
        )
        meters = list(session())
        assert all(isinstance(_, Meter) for _ in meters), repr(meters)
        return meters

    def generate_offset_kernel_to_denominator(
        self, denominator: int
    ) -> "MetricAccentKernel":
        r"""
        Generates MAK (dictionary) of all offsets in ``self`` up to
        ``denominator``.

        Keys of MAK are offsets.

        Values of MAK are normalized weights of those offsets.

        This is useful for testing how strongly a collection of offsets
        responds to a given meter.

        ..  container:: example

            >>> rtc = abjad.meter.make_best_guess_rtc((4, 4))
            >>> meter = abjad.Meter(rtc)
            >>> kernel = meter.generate_offset_kernel_to_denominator(8)
            >>> for offset, weight in sorted(kernel.kernel.items()):
            ...     print(f"{offset!r}\t{weight!r}")
            ...
            Offset((0, 1))	Fraction(3, 16)
            Offset((1, 8))	Fraction(1, 16)
            Offset((1, 4))	Fraction(1, 8)
            Offset((3, 8))	Fraction(1, 16)
            Offset((1, 2))	Fraction(1, 8)
            Offset((5, 8))	Fraction(1, 16)
            Offset((3, 4))	Fraction(1, 8)
            Offset((7, 8))	Fraction(1, 16)
            Offset((1, 1))	Fraction(3, 16)

        """
        assert _math.is_positive_integer_power_of_two(denominator // self.denominator)
        inventory = list(self.depthwise_offset_inventory)
        for offset_tuple in inventory:
            assert isinstance(offset_tuple, tuple)
            assert all(isinstance(_, _duration.Offset) for _ in offset_tuple)
        old_flag_count = _duration.Duration(1, self.denominator).flag_count
        new_flag_count = _duration.Duration(1, denominator).flag_count
        extra_depth = new_flag_count - old_flag_count
        assert isinstance(extra_depth, int), repr(extra_depth)
        for _ in range(extra_depth):
            old_offsets = inventory[-1]
            new_offsets = []
            for first_offset, second_offset in _sequence.nwise(old_offsets):
                new_offsets.append(first_offset)
                new_offsets.append((first_offset + second_offset) / 2)
            new_offsets.append(old_offsets[-1])
            inventory.append(tuple(new_offsets))
        total = 0
        offset_to_weight = {}
        for offset_tuple in inventory:
            for offset in offset_tuple:
                if offset not in offset_to_weight:
                    offset_to_weight[offset] = fractions.Fraction(0)
                offset_to_weight[offset] += fractions.Fraction(1)
                total += 1
        for offset, count in offset_to_weight.items():
            offset_to_weight[offset] = fractions.Fraction(count, total)
        return MetricAccentKernel(offset_to_weight)

    def rewrite(
        self,
        components: typing.Sequence[_score.Component],
        *,
        boundary_depth: int | None = None,
        initial_offset: _duration.Offset = _duration.Offset(0),
        maximum_dot_count: int | None = None,
        rewrite_tuplets: bool = True,
    ) -> None:
        r"""
        Rewrites ``components`` according to ``meter``.

        ..  container:: example

            Rewrites the contents of a measure in a staff using the default meter for
            that measure's time signature:

            >>> lily_string = "| 2/4 c'2 ~ |"
            >>> lily_string += "| 4/4 c'32 d'2.. ~ d'16 e'32 ~ |"
            >>> lily_string += "| 2/4 e'2 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff[:] = container
            >>> score = abjad.Score([staff], name="Score")
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

            >>> rtc = abjad.meter.make_best_guess_rtc((4, 4))
            >>> meter = abjad.Meter(rtc)
            >>> print(meter.pretty_rtm_format)
            (4/4 (
                1/4
                1/4
                1/4
                1/4))

            >>> meter.rewrite(staff[1][:])
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
            >>> score = abjad.Score([staff], name="Score")
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

            >>> string = '(4/4 ((2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'
            >>> rtc = abjad.rhythmtrees.parse(string)[0]
            >>> meter = abjad.Meter(rtc)
            >>> print(meter.pretty_rtm_format) # doctest: +SKIP
            (4/4 (
                (2/4 (
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))))

            >>> meter.rewrite(staff[1][:])
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

            Limit the maximum number of dots per leaf using ``maximum_dot_count``:

            >>> lily_string = "| 3/4 c'32 d'8 e'8 fs'4... |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> score = abjad.Score([staff], name="Score")
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
            >>> time_signature = abjad.get.indicator(measure[0], abjad.TimeSignature)
            >>> rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(measure[:])
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

            Constraining the ``maximum_dot_count`` to 2:

            >>> lily_string = "| 3/4 c'32 d'8 e'8 fs'4... |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> score = abjad.Score([staff], name="Score")
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(measure[0], abjad.TimeSignature)
            >>> rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(measure[:], maximum_dot_count=2)
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

            Constraining the ``maximum_dot_count`` to 1:

            >>> lily_string = "| 3/4 c'32 d'8 e'8 fs'4... |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> score = abjad.Score([staff], name="Score")
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(measure[0], abjad.TimeSignature)
            >>> rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(measure[:], maximum_dot_count=1)
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

            Constraining the ``maximum_dot_count`` to 0:

            >>> lily_string = "| 3/4 c'32 d'8 e'8 fs'4... |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> score = abjad.Score([staff], name="Score")
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(measure[0], abjad.TimeSignature)
            >>> rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(measure[:], maximum_dot_count=0)
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

            Split logical ties at different depths of the ``Meter``, if those logical
            ties cross any offsets at that depth, but do not also both begin and end at
            any of those offsets.

            Consider the default meter for ``9/8``:

            >>> rtc = abjad.meter.make_best_guess_rtc((9, 8))
            >>> meter = abjad.Meter(rtc)
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

            We can establish that meter without specifying a ``boundary_depth``:

            >>> lily_string = "| 9/8 c'2 d'2 e'8 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> score = abjad.Score([staff], name="Score")
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
            >>> time_signature = abjad.get.indicator(measure[0], abjad.TimeSignature)
            >>> rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(measure[:])
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

            With a ``boundary_depth`` of 1 logical ties which cross any offsets
            created by nodes with a depth of 1 in this Meter's rhythm tree --
            i.e. 0/8,  3/8, 6/8 and 9/8 -- which do not also begin and end at
            any of those offsets, will be split:

            >>> lily_string = "| 9/8 c'2 d'2 e'8 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> score = abjad.Score([staff], name="Score")
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(measure[0], abjad.TimeSignature)
            >>> rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(measure[:], boundary_depth=1)
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

            For this ``9/8`` meter, and this input notation, a ``boundary_depth`` of
            2 causes no change, as all logical ties already align to multiples of
            1/8:

            >>> lily_string = "| 9/8 c'2 d'2 e'8 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> score = abjad.Score([staff], name="Score")
            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(measure[0], abjad.TimeSignature)
            >>> rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(measure[:], boundary_depth=2)
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

            In order to see the different time signatures on each staff, we need to move
            some engravers from the Score context to the Staff context:

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
            ...         time_signature = abjad.get.indicator(leaf, abjad.TimeSignature)
            ...         rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            ...         meter = abjad.Meter(rtc)
            ...         meter.rewrite(container[:])
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

            Here we reestablish meter at a boundary depth of 1:

            >>> for staff in score:
            ...     for container in staff:
            ...         leaf = abjad.get.leaf(container, 0)
            ...         time_signature = abjad.get.indicator(leaf, abjad.TimeSignature)
            ...         rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            ...         meter = abjad.Meter(rtc)
            ...         meter.rewrite(container[:], boundary_depth=1)
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

            Note that the two time signatures are much more clearly disambiguated above.

        ..  container:: example

            Establishing meter recursively in measures with nested tuplets:

            >>> lily_string = "| 4/4 c'16 ~ c'4 d'8. ~ "
            >>> lily_string += "2/3 { d'8. ~ 3/5 { d'16 e'8. f'16 ~ } } "
            >>> lily_string += "f'4 |"
            >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(lily_string)
            >>> staff = abjad.Staff()
            >>> staff.append(container)
            >>> score = abjad.Score([staff], name="Score")
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
                        \tuplet 3/2
                        {
                            d'8.
                            ~
                            \tweak text #tuplet-number::calc-fraction-text
                            \tuplet 5/3
                            {
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
            contain containers, like tuplets or containers, ``abjad.Meter.rewrite()``
            will recurse into those containers, treating them as measures whose
            time signature is derived from the preprolated duration of the
            container's contents:

            >>> measure = staff[0]
            >>> time_signature = abjad.get.indicator(measure[0], abjad.TimeSignature)
            >>> rtc = abjad.meter.make_best_guess_rtc(time_signature.pair)
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(measure[:], boundary_depth=1)
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
                        \tuplet 3/2
                        {
                            d'8
                            ~
                            d'16
                            ~
                            \tweak text #tuplet-number::calc-fraction-text
                            \tuplet 5/3
                            {
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

            Default rewrite behavior doesn't subdivide the first note in this measure
            because the first note in the measure starts at the beginning of a level-0
            beat in meter:

            >>> staff = abjad.Staff("c'4.. c'16 ~ c'4")
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
            >>> rtc = abjad.meter.make_best_guess_rtc((6, 8))
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(staff[:])
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

            Setting boundary depth to 1 subdivides the first note in this measure:

            >>> staff = abjad.Staff("c'4.. c'16 ~ c'4")
            >>> score = abjad.Score([staff], name="Score")
            >>> abjad.attach(abjad.TimeSignature((6, 8)), staff[0])
            >>> rtc = abjad.meter.make_best_guess_rtc((6, 8))
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(staff[:], boundary_depth=1)
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

        ..  container:: example

            Rewrites notes and tuplets:

            >>> lily_string = r"c'8 ~ c'8 ~ c'8 \times 6/7 { c'4. r16 }"
            >>> lily_string += r" \times 6/7 { r16 c'4. } c'8 ~ c'8 ~ c'8"
            >>> staff = abjad.Staff(lily_string)
            >>> score = abjad.Score([staff], name="Score")
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
                    \tuplet 7/6
                    {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 7/6
                    {
                        r16
                        c'4.
                    }
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                }

            >>> rtc = abjad.meter.make_best_guess_rtc((6, 4))
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(staff[:], boundary_depth=1)
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 6/4
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 7/6
                    {
                        c'8.
                        ~
                        c'8
                        ~
                        c'16
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 7/6
                    {
                        r16
                        c'8
                        ~
                        c'4
                    }
                    c'4.
                }

            The tied note rewriting is good while the tuplet rewriting could use some
            adjustment.

            Rewrites notes but not tuplets:

            >>> lily_string = r"c'8 ~ c'8 ~ c'8 \times 6/7 { c'4. r16 }"
            >>> lily_string += r" \times 6/7 { r16 c'4. } c'8 ~ c'8 ~ c'8"
            >>> staff = abjad.Staff(lily_string)
            >>> score = abjad.Score([staff], name="Score")
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
                    \tuplet 7/6
                    {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 7/6
                    {
                        r16
                        c'4.
                    }
                    c'8
                    ~
                    c'8
                    ~
                    c'8
                }

            >>> rtc = abjad.meter.make_best_guess_rtc((6, 4))
            >>> meter = abjad.Meter(rtc)
            >>> meter.rewrite(
            ...     staff[:],
            ...     boundary_depth=1,
            ...     rewrite_tuplets=False,
            ... )
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> string = abjad.lilypond(staff)
                >>> print(string)
                \new Staff
                {
                    \time 6/4
                    c'4.
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 7/6
                    {
                        c'4.
                        r16
                    }
                    \tweak text #tuplet-number::calc-fraction-text
                    \tuplet 7/6
                    {
                        r16
                        c'4.
                    }
                    c'4.
                }

        """
        assert all(isinstance(_, _score.Component) for _ in components)
        if boundary_depth is not None:
            assert isinstance(boundary_depth, int)
        assert isinstance(initial_offset, _duration.Offset), repr(initial_offset)
        if maximum_dot_count is not None:
            assert isinstance(maximum_dot_count, int)
            assert 0 <= maximum_dot_count
        assert isinstance(rewrite_tuplets, bool)

        def recurse(
            logical_tie: _select.LogicalTie,
            boundary_depth: int | None = None,
            boundary_offsets=(),
            depth: int = 0,
        ) -> None:
            assert isinstance(logical_tie, _select.LogicalTie), repr(logical_tie)
            assert isinstance(boundary_offsets, tuple), repr(boundary_offsets)
            offsets = _get_offsets_at_depth(depth, offset_inventory)
            durations = [_._get_preprolated_duration() for _ in logical_tie]
            logical_tie_duration = sum(durations)
            logical_tie_timespan = _getlib._get_timespan(logical_tie)
            logical_tie_start_offset = logical_tie_timespan.start_offset
            logical_tie_stop_offset = logical_tie_timespan.stop_offset
            logical_tie_starts_in_offsets = logical_tie_start_offset in offsets
            logical_tie_stops_in_offsets = logical_tie_stop_offset in offsets
            if not _is_acceptable_logical_tie(
                logical_tie_duration=logical_tie_duration,
                logical_tie_starts_in_offsets=logical_tie_starts_in_offsets,
                logical_tie_stops_in_offsets=logical_tie_stops_in_offsets,
                maximum_dot_count=maximum_dot_count,
            ):
                split_offset = None
                offsets = _get_offsets_at_depth(depth, offset_inventory)
                # if the logical tie's start aligns, take the latest possible offset
                if logical_tie_starts_in_offsets:
                    offsets = tuple(reversed(offsets))
                for offset in offsets:
                    if logical_tie_start_offset < offset < logical_tie_stop_offset:
                        split_offset = offset
                        break
                if split_offset is not None:
                    split_offset -= logical_tie_start_offset
                    shards = _mutate.split(logical_tie[:], [split_offset])
                    logical_ties = [_select.LogicalTie(_) for _ in shards]
                    for logical_tie in logical_ties:
                        recurse(
                            logical_tie,
                            boundary_depth=boundary_depth,
                            boundary_offsets=boundary_offsets,
                            depth=depth,
                        )
                else:
                    recurse(
                        logical_tie,
                        boundary_depth=boundary_depth,
                        boundary_offsets=boundary_offsets,
                        depth=depth + 1,
                    )
            elif _is_boundary_crossing_logical_tie(
                logical_tie_start_offset,
                logical_tie_stop_offset,
                boundary_depth=boundary_depth,
                boundary_offsets=boundary_offsets,
            ):
                offsets = boundary_offsets
                if logical_tie_start_offset in boundary_offsets:
                    offsets = tuple(reversed(boundary_offsets))
                split_offset = None
                for offset in offsets:
                    if logical_tie_start_offset < offset < logical_tie_stop_offset:
                        split_offset = offset
                        break
                assert split_offset is not None
                split_offset -= logical_tie_start_offset
                shards = _mutate.split(logical_tie[:], [split_offset])
                logical_ties = [_select.LogicalTie(shard) for shard in shards]
                for logical_tie in logical_ties:
                    recurse(
                        logical_tie,
                        boundary_depth=boundary_depth,
                        boundary_offsets=boundary_offsets,
                        depth=depth,
                    )
            else:
                _mutate._fuse(logical_tie[:])

        nongrace_components = []
        for component in components:
            if not isinstance(component, _score.IndependentAfterGraceContainer):
                nongrace_components.append(component)
        first_start_offset = nongrace_components[0]._get_timespan().start_offset
        last_start_offset = nongrace_components[-1]._get_timespan().start_offset
        difference = last_start_offset - first_start_offset + initial_offset
        assert difference < self.implied_time_signature.duration
        # build offset inventory, adjusted for initial offset and prolation
        first_offset = components[0]._get_timespan().start_offset
        first_offset -= initial_offset
        if components[0]._parent is None:
            prolation = fractions.Fraction(1)
        else:
            parentage = _parentage.Parentage(components[0]._parent)
            prolation = parentage.prolation
        offset_inventory = []
        for offsets in self.depthwise_offset_inventory:
            offsets = [(_ * prolation) + first_offset for _ in offsets]
            offset_inventory.append(tuple(offsets))
        # build boundary offset inventory, if applicable
        if boundary_depth is not None:
            boundary_offsets = offset_inventory[boundary_depth]
        else:
            boundary_offsets = ()
        # cache results of iterator; we'll be mutating the underlying collection
        iterator = _iterate_rewrite_inputs(components)
        items = tuple(iterator)
        for item in items:
            if isinstance(item, _select.LogicalTie):
                recurse(
                    item,
                    boundary_depth=boundary_depth,
                    boundary_offsets=boundary_offsets,
                    depth=0,
                )
            elif isinstance(item, _score.Tuplet) and not rewrite_tuplets:
                pass
            else:
                duration = sum([_._get_preprolated_duration() for _ in item])
                if duration.numerator == 1:
                    denominator = 4 * duration.denominator
                    pair = _duration.with_denominator(duration, denominator)
                else:
                    pair = duration.pair
                rtc_ = make_best_guess_rtc(pair)
                sub_metrical_hierarchy = Meter(rtc_)
                sub_boundary_depth: int | None = 1
                if boundary_depth is None:
                    sub_boundary_depth = None
                sub_metrical_hierarchy.rewrite(
                    item[:],
                    boundary_depth=sub_boundary_depth,
                    maximum_dot_count=maximum_dot_count,
                )


def _get_offsets_at_depth(
    depth, offset_inventory: list[tuple[_duration.Offset, ...]]
) -> tuple[_duration.Offset, ...]:
    assert all(isinstance(_, tuple) for _ in offset_inventory)
    if depth < len(offset_inventory):
        return offset_inventory[depth]
    while len(offset_inventory) <= depth:
        new_offsets = []
        old_offsets = offset_inventory[-1]
        for first, second in _sequence.nwise(old_offsets):
            new_offsets.append(first)
            difference = second - first
            half = (first + second) / 2
            if _duration.Duration(1, 8) < difference:
                new_offsets.append(half)
            else:
                one_quarter = (first + half) / 2
                three_quarters = (half + second) / 2
                new_offsets.append(one_quarter)
                new_offsets.append(half)
                new_offsets.append(three_quarters)
        new_offsets.append(old_offsets[-1])
        offset_inventory.append(tuple(new_offsets))
    result = offset_inventory[depth]
    assert isinstance(result, tuple)
    assert all(isinstance(_, _duration.Offset) for _ in result), repr(result)
    return result


def _is_acceptable_logical_tie(
    logical_tie_duration: _duration.Duration,
    logical_tie_starts_in_offsets: bool = False,
    logical_tie_stops_in_offsets: bool = False,
    maximum_dot_count: int | None = None,
) -> bool:
    assert isinstance(logical_tie_duration, _duration.Duration)
    assert isinstance(logical_tie_starts_in_offsets, bool)
    assert isinstance(logical_tie_stops_in_offsets, bool)
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


def _is_boundary_crossing_logical_tie(
    logical_tie_start_offset: _duration.Offset,
    logical_tie_stop_offset: _duration.Offset,
    boundary_depth: int | None = None,
    boundary_offsets: tuple[_duration.Offset, ...] = (),
) -> bool:
    assert isinstance(logical_tie_start_offset, _duration.Offset)
    assert isinstance(logical_tie_stop_offset, _duration.Offset)
    if boundary_depth is None:
        return False
    if not any(
        logical_tie_start_offset < _ < logical_tie_stop_offset for _ in boundary_offsets
    ):
        return False
    if (
        logical_tie_start_offset in boundary_offsets
        and logical_tie_stop_offset in boundary_offsets
    ):
        return False
    return True


def _iterate_rewrite_inputs(
    argument: typing.Sequence[_score.Component],
) -> typing.Iterator[_select.LogicalTie | _score.Container]:
    r"""
    Iterates topmost masked logical ties, rest groups and containers in
    ``argument``, masked by ``argument``.

    ..  container:: example

        >>> string = "! 2/4 c'4 d'4 ~ !"
        >>> string += "! 4/4 d'8. r16 r8. e'16 ~ "
        >>> string += "2/3 { e'8 ~ e'8 f'8 ~ } f'4 ~ !"
        >>> string += "! 4/4 f'8 g'8 ~ g'4 a'4 ~ a'8 b'8 ~ !"
        >>> string += "! 2/4 b'4 c''4 !"
        >>> string = string.replace('!', '|')
        >>> container = abjad.parsers.reduced.parse_reduced_ly_syntax(string)
        >>> staff = abjad.Staff()
        >>> score = abjad.Score([staff], name="Score")
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
                    \tuplet 3/2
                    {
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

        >>> for x in abjad.meter._iterate_rewrite_inputs(staff[0]):
        ...     x
        ...
        LogicalTie(items=[Note("c'4")])
        LogicalTie(items=[Note("d'4")])

        >>> for x in abjad.meter._iterate_rewrite_inputs(staff[1]):
        ...     x
        ...
        LogicalTie(items=[Note("d'8.")])
        LogicalTie(items=[Rest('r16'), Rest('r8.')])
        LogicalTie(items=[Note("e'16")])
        Tuplet('3:2', "e'8 e'8 f'8")
        LogicalTie(items=[Note("f'4")])

        >>> for x in abjad.meter._iterate_rewrite_inputs(staff[2]):
        ...     x
        ...
        LogicalTie(items=[Note("f'8")])
        LogicalTie(items=[Note("g'8"), Note("g'4")])
        LogicalTie(items=[Note("a'4"), Note("a'8")])
        LogicalTie(items=[Note("b'8")])

        >>> for x in abjad.meter._iterate_rewrite_inputs(staff[3]):
        ...     x
        ...
        LogicalTie(items=[Note("b'4")])
        LogicalTie(items=[Note("c''4")])

    """
    last_tie = None
    current_leaf_group: list[_score.Leaf] | None = None
    current_leaf_group_is_silent = False
    for component in argument:
        assert isinstance(component, _score.Component)
        if isinstance(component, _score.Note | _score.Chord):
            this_tie_leaves = _iterlib._get_logical_tie_leaves(component)
            this_tie = _select.LogicalTie(this_tie_leaves)
            if current_leaf_group is None:
                current_leaf_group = []
            elif (
                current_leaf_group_is_silent or this_tie is None or last_tie != this_tie
            ):
                yield _select.LogicalTie(current_leaf_group)
                current_leaf_group = []
            current_leaf_group_is_silent = False
            current_leaf_group.append(component)
            last_tie = this_tie
        elif isinstance(component, _score.Rest | _score.Skip):
            if current_leaf_group is None:
                current_leaf_group = []
            elif not current_leaf_group_is_silent:
                yield _select.LogicalTie(current_leaf_group)
                current_leaf_group = []
            current_leaf_group_is_silent = True
            current_leaf_group.append(component)
            last_tie = None
        elif isinstance(component, _score.Container):
            if current_leaf_group is not None:
                yield _select.LogicalTie(current_leaf_group)
                current_leaf_group = None
                last_tie = None
            yield component
        else:
            raise Exception(f"unhandled component: {component!r}.")
    if current_leaf_group is not None:
        yield _select.LogicalTie(current_leaf_group)


def illustrate_meter_list(
    meter_list: list["Meter"],
    denominator: int = 16,
    range_: tuple | None = None,
    scale: float = 1.0,
) -> _lilypondfile.LilyPondFile:
    r"""
    Illustrates meters.

    ..  container:: example

        The PNG image that would be rendered below fails to draw vertical lines
        in Postscript. But the output renders correctly as a PDF. To see the
        effect of this function, paste the excerpt below into a test file and
        call LilyPond on that test file:

        >>> pairs = [(3, 4), (5, 16), (7, 8)]
        >>> rtcs = [abjad.meter.make_best_guess_rtc(_) for _ in pairs]
        >>> meters = [abjad.Meter(_) for _ in rtcs]
        >>> lilypond_file = abjad.meter.illustrate_meter_list(meters, scale=0.5)

        ..  docs::

            >>> lilypond_file = abjad.meter.illustrate_meter_list(meters)
            >>> markup = lilypond_file.items[0]
            >>> string = abjad.lilypond(markup)
            >>> print(string)
            \markup
            \column
            {
            \combine
            \combine
            \translate #'(1.0 . 1)
            \sans \fontsize #-3 \center-align \fraction 3 4
            \translate #'(49.38709677419355 . 1)
            \sans \fontsize #-3 \center-align \fraction 5 16
            \translate #'(69.54838709677419 . 1)
            \sans \fontsize #-3 \center-align \fraction 7 8
            \combine
            \postscript
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
            "
            \postscript
            #"
            1 -2 moveto
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
            stroke
            "
            }

    """
    assert all(isinstance(_, Meter) for _ in meter_list), repr(meter_list)
    assert isinstance(denominator, int), repr(denominator)
    if range_ is not None:
        assert isinstance(range_, tuple), repr(range_)
    assert isinstance(scale, float), repr(scale)
    durations = [_.duration for _ in meter_list]
    total_duration = sum(durations)
    offsets = _math.cumulative_sums(durations, start=0)
    timespans = _timespan.TimespanList()
    for one, two in _sequence.nwise(offsets):
        timespan = _timespan.Timespan(start_offset=one, stop_offset=two)
        timespans.append(timespan)
    if range_ is not None:
        minimum, maximum = range_
    else:
        minimum, maximum = 0, total_duration
    minimum = float(_duration.Offset(minimum))
    maximum = float(_duration.Offset(maximum))
    if scale is None:
        scale = 1.0
    assert 0 < scale
    postscript_scale = 125.0 / (maximum - minimum)
    postscript_scale *= float(scale)
    postscript_x_offset = (minimum * postscript_scale) - 1
    timespan_markup = _timespan._make_timespan_list_markup(
        timespans,
        postscript_x_offset,
        postscript_scale,
        draw_offsets=False,
    )
    postscript_strings = []
    rational_x_offset = _duration.Offset(0)
    for meter in meter_list:
        kernel_denominator = denominator or meter.denominator
        kernel = MetricAccentKernel.from_meter(meter, kernel_denominator)
        for offset, weight in sorted(kernel.kernel.items()):
            assert isinstance(weight, fractions.Fraction)
            weight_as_float = float(weight) * -40
            ps_x_offset = float(rational_x_offset + offset)
            ps_x_offset *= postscript_scale
            ps_x_offset += 1
            postscript_strings.append(f"{_timespan._fpa(ps_x_offset)} -2 moveto")
            postscript_strings.append(f"0 {_timespan._fpa(weight_as_float)} rlineto")
            postscript_strings.append("stroke")
        rational_x_offset += meter.duration
    fraction_pairs = []
    for meter, offset in zip(meter_list, offsets):
        numerator, denominator = meter.numerator, meter.denominator
        x_translation = float(offset) * postscript_scale
        x_translation -= postscript_x_offset
        top_string = rf"\translate #'({x_translation} . 1)"
        bottom_string = r"\sans \fontsize #-3 \center-align"
        bottom_string = bottom_string + rf" \fraction {numerator} {denominator}"
        pair = (top_string, bottom_string)
        fraction_pairs.append(pair)
    fraction_strings = []
    fraction_strings.append(fraction_pairs[0][0])
    fraction_strings.append(fraction_pairs[0][1])
    for pair in fraction_pairs[1:]:
        fraction_strings.insert(0, r"\combine")
        fraction_strings.append(pair[0])
        fraction_strings.append(pair[1])
    strings = []
    strings.append(r"\markup")
    strings.append(r"\column")
    strings.append("{")
    strings.extend(fraction_strings)
    strings.append(r"\combine")
    strings.append(timespan_markup.string)
    strings.append(r"\postscript")
    strings.append('#"')
    strings.extend(postscript_strings)
    strings.append('"')
    strings.append("}")
    string = "\n".join(strings)
    markup = _indicators.Markup(string)
    lilypond_file = _lilypondfile.LilyPondFile()
    lilypond_file.items.append(markup)
    return lilypond_file


class MetricAccentKernel:
    """
    Metric accent kernel.

    ..  container:: example

        >>> rtc = abjad.meter.make_best_guess_rtc((7, 8))
        >>> hierarchy = abjad.Meter(rtc)
        >>> kernel = hierarchy.generate_offset_kernel_to_denominator(8)
        >>> for offset, weight in kernel.kernel.items():
        ...     print(f"{offset!r}: {weight!r}")
        Offset((0, 1)): Fraction(3, 14)
        Offset((7, 8)): Fraction(3, 14)
        Offset((3, 8)): Fraction(1, 7)
        Offset((5, 8)): Fraction(1, 7)
        Offset((1, 8)): Fraction(1, 14)
        Offset((1, 4)): Fraction(1, 14)
        Offset((1, 2)): Fraction(1, 14)
        Offset((3, 4)): Fraction(1, 14)

    Call the kernel against an expression from which offsets can be counted to
    receive an impulse-response:

    ..  container:: example

        >>> pairs = [(0, 8), (1, 8), (1, 8), (3, 8)]
        >>> offsets = [abjad.Offset(_) for _ in pairs]
        >>> offset_counter = abjad.OffsetCounter(offsets)
        >>> kernel(offset_counter)
        Fraction(1, 2)

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_kernel", "_offsets")

    ### INITIALIZER ###

    def __init__(self, kernel: dict | None = None):
        kernel = kernel or {}
        assert isinstance(kernel, dict)
        for key, value in kernel.items():
            assert isinstance(key, _duration.Offset)
            assert isinstance(value, fractions.Fraction)
        self._kernel = kernel.copy()
        offsets = tuple(sorted(self._kernel))
        self._offsets = offsets

    ### SPECIAL METHODS ###

    def __call__(self, offset_counter: _timespan.OffsetCounter) -> fractions.Fraction:
        r"""
        Calls metric accent kernal on ``offset_counter``.

        ..  container:: example

            >>> upper_staff = abjad.Staff("c'8 d'4. e'8 f'4.")
            >>> lower_staff = abjad.Staff(r"\clef bass c4 b,4 a,2")
            >>> score = abjad.Score([upper_staff, lower_staff])
            >>> abjad.show(score) # doctest: +SKIP

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

            >>> rtc = abjad.meter.make_best_guess_rtc((4, 4))
            >>> meter = abjad.Meter(rtc)
            >>> kernel = abjad.MetricAccentKernel.from_meter(meter)
            >>> offset_counter = abjad.OffsetCounter(score)
            >>> kernel(offset_counter)
            Fraction(10, 33)

        """
        assert isinstance(offset_counter, _timespan.OffsetCounter), repr(offset_counter)
        response = fractions.Fraction(0, 1)
        for offset, count in offset_counter.items.items():
            if offset in self._kernel:
                weight = self._kernel[offset]
                weighted_count = weight * count
                response += weighted_count
        assert isinstance(response, fractions.Fraction), repr(response)
        return response

    def __eq__(self, argument) -> bool:
        """
        Is true when ``argument`` is a metric accent kernal with a kernal equal
        to that of ``self``.
        """
        if isinstance(argument, type(self)):
            if self.kernel == argument.kernel:
                if self.duration == argument.duration:
                    return True
        return False

    def __hash__(self) -> int:
        """
        Hashes metric accent kernel.
        """
        return super().__hash__()

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}(kernel={self.kernel})"

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self) -> _duration.Duration:
        """
        Gets duration.
        """
        if self._offsets:
            return _duration.Duration(self._offsets[-1])
        else:
            return _duration.Duration(0)

    @property
    def kernel(self) -> dict[_duration.Offset, fractions.Fraction]:
        """
        The kernel dictionary.
        """
        return self._kernel.copy()

    ### PUBLIC METHODS ###

    @staticmethod
    def from_meter(meter: Meter, denominator: int = 32) -> "MetricAccentKernel":
        """
        Create a metric accent kernel from ``meter``.
        """
        assert isinstance(meter, Meter), repr(meter)
        assert isinstance(denominator, int), repr(denominator)
        return meter.generate_offset_kernel_to_denominator(denominator=denominator)


class _MeterFittingSession:
    """
    Meter-fitting session.

    Used internally by ``Meter.fit_meters()``.
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
        kernel_denominator: int = 32,
        maximum_run_length: int | None = None,
        meters: typing.Sequence[Meter] = (),
        offset_counter: _timespan.OffsetCounter = _timespan.OffsetCounter(),
    ) -> None:
        assert isinstance(kernel_denominator, int), repr(kernel_denominator)
        if maximum_run_length is not None:
            assert isinstance(maximum_run_length, int), repr(maximum_run_length)
            assert 0 < maximum_run_length
        assert all(isinstance(_, Meter) for _ in meters), repr(meters)
        assert isinstance(offset_counter, _timespan.OffsetCounter), repr(offset_counter)
        assert isinstance(offset_counter, _timespan.OffsetCounter), repr(offset_counter)
        self._cached_offset_counters: dict = {}
        self._maximum_run_length = maximum_run_length
        self._meters = tuple(meters)
        self._offset_counter = offset_counter
        self._ordered_offsets = tuple(sorted(self.offset_counter.items))
        self._kernel_denominator = kernel_denominator
        self._kernels = {}
        for meter in self._meters:
            kernel = meter.generate_offset_kernel_to_denominator(
                self._kernel_denominator
            )
            self._kernels[kernel] = meter
        mak = sorted(self._kernels, key=lambda _: _.duration)[-1]
        assert isinstance(mak, MetricAccentKernel), repr(mak)
        self._longest_kernel = mak

    ### SPECIAL METHODS ###

    def __call__(self) -> list[Meter]:
        """
        Fits meters.
        """
        selected_kernels: list[MetricAccentKernel] = []
        current_offset = _duration.Offset(0)
        while current_offset < self.ordered_offsets[-1]:
            kernel_scores: list[_MeterFittingSession.KernelScore] = []
            kernels = self._get_kernels(selected_kernels)
            offset_counter = self._get_offset_counter_at(current_offset)
            assert isinstance(offset_counter, _timespan.OffsetCounter), repr(
                offset_counter
            )
            if not offset_counter:
                winning_kernel = self.longest_kernel
                assert isinstance(winning_kernel, MetricAccentKernel)
                if selected_kernels:
                    winning_kernel = selected_kernels[-1]
                    assert isinstance(winning_kernel, MetricAccentKernel)
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
                assert isinstance(winning_kernel, MetricAccentKernel)
            selected_kernels.append(winning_kernel)
            current_offset += winning_kernel.duration
        selected_meters = [self.kernels[_] for _ in selected_kernels]
        assert all(isinstance(_, Meter) for _ in selected_meters), repr(selected_meters)
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
        lookahead_score = sum(lookahead_scores)
        return lookahead_score

    def _get_offset_counter_at(self, start_offset) -> _timespan.OffsetCounter:
        if start_offset in self.cached_offset_counters:
            return _timespan.OffsetCounter(self.cached_offset_counters[start_offset])
        offset_to_weight: dict[_duration.Offset, fractions.Fraction] = {}
        assert self.longest_kernel is not None
        stop_offset = start_offset + self.longest_kernel.duration
        index = bisect.bisect_left(self.ordered_offsets, start_offset)
        if index == len(self.ordered_offsets):
            return _timespan.OffsetCounter(offset_to_weight)
        offset = self.ordered_offsets[index]
        while offset <= stop_offset:
            count = self.offset_counter.items[offset]
            offset_to_weight[offset - start_offset] = count
            index += 1
            if index == len(self.ordered_offsets):
                break
            offset = self.ordered_offsets[index]
        self.cached_offset_counters[start_offset] = offset_to_weight
        offset_counter = _timespan.OffsetCounter(offset_to_weight)
        return offset_counter

    ### PUBLIC PROPERTIES ###

    @property
    def cached_offset_counters(self) -> dict:
        """
        Gets cached offset counters
        """
        return self._cached_offset_counters

    @property
    def kernel_denominator(self) -> int:
        """
        Gets kernel denominator.
        """
        return self._kernel_denominator

    @property
    def kernels(self) -> dict:
        """
        Gets kernels-to-meter dictionary.
        """
        return self._kernels

    @property
    def longest_kernel(self) -> MetricAccentKernel:
        """
        Gets longest kernel.
        """
        return self._longest_kernel

    @property
    def maximum_run_length(self) -> int | None:
        """
        Gets maximum meter repetitions.
        """
        return self._maximum_run_length

    @property
    def meters(self) -> tuple[Meter, ...]:
        """
        Gets meters.
        """
        return self._meters

    @property
    def offset_counter(self) -> _timespan.OffsetCounter:
        """
        Gets offset counter.
        """
        return self._offset_counter

    @property
    def ordered_offsets(self) -> tuple[_duration.Offset, ...]:
        """
        Gets ordered offsets.
        """
        return self._ordered_offsets


def make_best_guess_rtc(
    pair: tuple[int, int], *, increase_monotonic: bool = False
) -> _rhythmtrees.RhythmTreeContainer:
    """
    Makes best-guess rhythm-tree container.

    Prime divisions greater than 3 are converted to sequences of 2, 3 and 4
    summing to that prime. Summands are arranged from greatest to least by
    default. This means that 5 becomes 3+2 and 7 becomes 3+2+2 in the examples
    below.

    ..  container:: example

        >>> rtc = abjad.meter.make_best_guess_rtc((2, 4))
        >>> print(rtc.pretty_rtm_format)
        (2/4 (
            1/4
            1/4))

        >>> rtc = abjad.meter.make_best_guess_rtc((3, 4))
        >>> print(rtc.pretty_rtm_format)
        (3/4 (
            1/4
            1/4
            1/4))

        >>> rtc = abjad.meter.make_best_guess_rtc((4, 4))
        >>> print(rtc.pretty_rtm_format)
        (4/4 (
            1/4
            1/4
            1/4
            1/4))

        >>> rtc = abjad.meter.make_best_guess_rtc((5, 4))
        >>> print(rtc.pretty_rtm_format)
        (5/4 (
            (3/4 (
                1/4
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

        >>> rtc = abjad.meter.make_best_guess_rtc((5, 4), increase_monotonic=True)
        >>> print(rtc.pretty_rtm_format)
        (5/4 (
            (2/4 (
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))))

        >>> rtc = abjad.meter.make_best_guess_rtc((6, 4))
        >>> print(rtc.pretty_rtm_format)
        (6/4 (
            (3/4 (
                1/4
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))))

        >>> rtc = abjad.meter.make_best_guess_rtc((7, 4))
        >>> print(rtc.pretty_rtm_format)
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

        >>> rtc = abjad.meter.make_best_guess_rtc((7, 4), increase_monotonic=True)
        >>> print(rtc.pretty_rtm_format)
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

        >>> rtc = abjad.meter.make_best_guess_rtc((8, 4))
        >>> print(rtc.pretty_rtm_format)
        (8/4 (
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

        >>> rtc = abjad.meter.make_best_guess_rtc((9, 4))
        >>> print(rtc.pretty_rtm_format)
        (9/4 (
            (3/4 (
                1/4
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))))

    ..  container:: example

        >>> rtc = abjad.meter.make_best_guess_rtc((2, 8))
        >>> print(rtc.pretty_rtm_format)
        (2/8 (
            1/8
            1/8))

        >>> rtc = abjad.meter.make_best_guess_rtc((3, 8))
        >>> print(rtc.pretty_rtm_format)
        (3/8 (
            1/8
            1/8
            1/8))

        >>> rtc = abjad.meter.make_best_guess_rtc((4, 8))
        >>> print(rtc.pretty_rtm_format)
        (4/8 (
            1/8
            1/8
            1/8
            1/8))

        >>> rtc = abjad.meter.make_best_guess_rtc((5, 8))
        >>> print(rtc.pretty_rtm_format)
        (5/8 (
            (3/8 (
                1/8
                1/8
                1/8))
            (2/8 (
                1/8
                1/8))))

        >>> rtc = abjad.meter.make_best_guess_rtc((5, 8), increase_monotonic=True)
        >>> print(rtc.pretty_rtm_format)
        (5/8 (
            (2/8 (
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))))

        >>> rtc = abjad.meter.make_best_guess_rtc((6, 8))
        >>> print(rtc.pretty_rtm_format)
        (6/8 (
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))))

        >>> rtc = abjad.meter.make_best_guess_rtc((7, 8))
        >>> print(rtc.pretty_rtm_format)
        (7/8 (
            (3/8 (
                1/8
                1/8
                1/8))
            (2/8 (
                1/8
                1/8))
            (2/8 (
                1/8
                1/8))))

        >>> rtc = abjad.meter.make_best_guess_rtc((7, 8), increase_monotonic=True)
        >>> print(rtc.pretty_rtm_format)
        (7/8 (
            (2/8 (
                1/8
                1/8))
            (2/8 (
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))))

        >>> rtc = abjad.meter.make_best_guess_rtc((8, 8))
        >>> print(rtc.pretty_rtm_format)
        (8/8 (
            (2/8 (
                1/8
                1/8))
            (2/8 (
                1/8
                1/8))
            (2/8 (
                1/8
                1/8))
            (2/8 (
                1/8
                1/8))))

        >>> rtc = abjad.meter.make_best_guess_rtc((9, 8))
        >>> print(rtc.pretty_rtm_format)
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

        >>> rtc = abjad.meter.make_best_guess_rtc((12, 8))
        >>> print(rtc.pretty_rtm_format)
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

    """
    assert isinstance(pair, tuple), repr(pair)
    assert all(isinstance(_, int) for _ in pair), repr(pair)
    assert isinstance(increase_monotonic, bool), repr(increase_monotonic)
    rtc = _rhythmtrees.RhythmTreeContainer(pair)
    numerator, denominator = pair
    numerator_factors = _math.factors(numerator)
    if 1 < len(numerator_factors) and numerator_factors[0] == numerator_factors[1] == 2:
        numerator_factors[0:2] = [4]

    def recurse(
        rtc: _rhythmtrees.RhythmTreeContainer,
        factors: typing.Sequence[int],
        denominator: int,
        *,
        increase_monotonic: bool = False,
    ) -> None:
        assert isinstance(rtc, _rhythmtrees.RhythmTreeContainer)
        assert all(isinstance(_, int) for _ in factors)
        assert isinstance(denominator, int)
        assert isinstance(increase_monotonic, bool)
        if factors:
            factor, factors = factors[0], factors[1:]
            pair = _duration.divide_pair(rtc.pair, factor)
            if factor in (2, 3, 4):
                if factors:
                    for _ in range(factor):
                        rtc_ = _rhythmtrees.RhythmTreeContainer(pair)
                        rtc.append(rtc_)
                        recurse(
                            rtc_,
                            factors,
                            denominator,
                            increase_monotonic=increase_monotonic,
                        )
                else:
                    for _ in range(factor):
                        pair_ = (1, denominator)
                        rtl = _rhythmtrees.RhythmTreeLeaf(pair_)
                        rtc.append(rtl)
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
                    assert isinstance(part, int)
                    pair_ = (part * pair[0], pair[1])
                    grouping = _rhythmtrees.RhythmTreeContainer(pair_)
                    if factors:
                        for _ in range(part):
                            rtc_ = _rhythmtrees.RhythmTreeContainer(pair)
                            grouping.append(rtc_)
                            recurse(
                                rtc_,
                                factors,
                                denominator,
                                increase_monotonic=increase_monotonic,
                            )
                    else:
                        for _ in range(part):
                            pair_ = (1, denominator)
                            rtl = _rhythmtrees.RhythmTreeLeaf(pair_)
                            grouping.append(rtl)
                    rtc.append(grouping)
        else:
            pair_ = (1, denominator)
            for _ in range(rtc.pair[0]):
                rtl = _rhythmtrees.RhythmTreeLeaf(pair_)
                rtc.append(rtl)

    recurse(
        rtc,
        numerator_factors,
        denominator,
        increase_monotonic=increase_monotonic,
    )
    return rtc
