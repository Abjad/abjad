"""
Tools for modeling musical meter.
"""

import bisect
import collections
import uqbar.graphs
import abjad.rhythmtrees
from abjad import core
from abjad import indicators as abjad_indicators
from abjad import mathtools
from abjad import system
from abjad.system.AbjadValueObject import AbjadValueObject
from abjad.utilities.TypedCounter import TypedCounter
from abjad.utilities.TypedList import TypedList


class Meter(AbjadValueObject):
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

        >>> graph(meter) # doctest: +SKIP

        `2/4` comprises two beats.

    ..  container:: example

        Triple meter:

        >>> meter = abjad.Meter((3, 4))
        >>> print(meter.pretty_rtm_format)
        (3/4 (
            1/4
            1/4
            1/4))

        >>> graph(meter) # doctest: +SKIP

        `3/4` comprises three beats.

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

        >>> graph(meter) # doctest: +SKIP

        `4/4` comprises four beats.

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

        >>> graph(meter) # doctest: +SKIP

        `6/8` comprises two beats of three parts each.

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

        >>> graph(meter) # doctest: +SKIP

        `12/8` comprises four beats of three parts each.

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

        >>> graph(meter) # doctest: +SKIP

        `5/4` comprises two unequal beats. By default unequal beats
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

        >>> graph(meter) # doctest: +SKIP

        `7/4` comprises three unequal beats. Beats are arranged from
        greatest to least by default.

    ..  container:: example

        The same asymmetric meter structured differently:

        >>> meter = abjad.Meter(
        ...     (7, 4),
        ...     decrease_monotonic=False,
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

        >>> graph(meter) # doctest: +SKIP

        `7/4` with beats arragned from least to greatest.

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

        >>> graph(meter) # doctest: +SKIP

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

        >>> graph(meter) # doctest: +SKIP

    Prime divisions greater than ``3`` are converted to sequences of ``2``
    and ``3`` summing to that prime. Summands are arranged from greatest
    to least by default. This means that ``5`` becomes ``3+2`` and ``7``
    becomes ``3+2+2`` in the examples above.
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_decrease_monotonic',
        '_denominator',
        '_numerator',
        '_preferred_boundary_depth',
        '_root_node',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        argument=None,
        decrease_monotonic=True,
        preferred_boundary_depth=None,
    ):

        argument = argument or (4, 4)
        assert isinstance(preferred_boundary_depth, (int, type(None)))
        self._preferred_boundary_depth = preferred_boundary_depth

        def recurse(
            node,
            factors,
            denominator,
            decrease_monotonic,
        ):
            if factors:
                factor, factors = factors[0], factors[1:]
                preprolated_duration = \
                    node.preprolated_duration.__div__(factor)
                #if factor in (2, 3, 4, 5):
                if factor in (2, 3, 4):
                    if factors:
                        for _ in range(factor):
                            child = abjad.rhythmtrees.RhythmTreeContainer(
                                preprolated_duration=preprolated_duration)
                            node.append(child)
                            recurse(
                                child,
                                factors,
                                denominator,
                                decrease_monotonic,
                                )
                    else:
                        for _ in range(factor):
                            node.append(
                                abjad.rhythmtrees.RhythmTreeLeaf(
                                    preprolated_duration=(1, denominator)))
                else:
                    parts = [3]
                    total = 3
                    while total < factor:
                        if decrease_monotonic:
                            parts.append(2)
                        else:
                            parts.insert(0, 2)
                        total += 2
                    for part in parts:
                        grouping = abjad.rhythmtrees.RhythmTreeContainer(
                            preprolated_duration=part * preprolated_duration)
                        if factors:
                            for _ in range(part):
                                child = abjad.rhythmtrees.RhythmTreeContainer(
                                    preprolated_duration=preprolated_duration)
                                grouping.append(child)
                                recurse(
                                    child,
                                    factors,
                                    denominator,
                                    decrease_monotonic,
                                    )
                        else:
                            for _ in range(part):
                                grouping.append(
                                    abjad.rhythmtrees.RhythmTreeLeaf(
                                        preprolated_duration=(1, denominator)))
                        node.append(grouping)
            else:
                node.extend([abjad.rhythmtrees.RhythmTreeLeaf(
                    preprolated_duration=(1, denominator))
                    for _ in range(node.preprolated_duration.numerator)])

        decrease_monotonic = bool(decrease_monotonic)

        try:
            numerator = argument.numerator
            denominator = argument.denominator
            is_fraction_like = True
        except AttributeError:
            is_fraction_like = False

        if isinstance(argument, type(self)):
            root = argument.root_node
            numerator, denominator = argument.numerator, argument.denominator
            decrease_monotonic = argument.decrease_monotonic

        elif isinstance(argument, (str, abjad.rhythmtrees.RhythmTreeContainer)):
            if isinstance(argument, str):
                parsed = abjad.rhythmtrees.RhythmTreeParser()(argument)
                assert len(parsed) == 1
                root = parsed[0]
            else:
                root = argument
            for node in [root] + list(root.depth_first()):
                assert node.prolation == 1
            numerator = root.preprolated_duration.numerator
            denominator = root.preprolated_duration.denominator

        elif (
            isinstance(argument, (tuple, core.Measure)) or
            is_fraction_like
        ):
            if isinstance(argument, tuple):
                fraction = mathtools.NonreducedFraction(argument)
            elif isinstance(argument, core.Measure):
                prototype = abjad_indicators.TimeSignature
                time_signature = argument._get_effective(prototype)
                fraction = mathtools.NonreducedFraction(
                    time_signature.numerator,
                    time_signature.denominator,
                    )
            else:
                fraction = mathtools.NonreducedFraction(
                    argument.numerator,
                    argument.denominator,
                    )
            numerator, denominator = fraction.numerator, fraction.denominator
            factors = mathtools.factors(numerator)
            # group two nested levels of 2s into a 4
            if 1 < len(factors) and factors[0] == factors[1] == 2:
                factors[0:2] = [4]
            root = abjad.rhythmtrees.RhythmTreeContainer(
                preprolated_duration=fraction)
            recurse(
                root,
                factors,
                denominator,
                decrease_monotonic,
                )

        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, argument)
            raise ValueError(message)

        self._root_node = root
        self._numerator = numerator
        self._denominator = denominator
        self._decrease_monotonic = decrease_monotonic

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a meter with an rtm format equal to that
        of this meter.

        Returns true or false.
        """
        return super().__eq__(argument)

    def __format__(self, format_specification=''):
        """
        Formats meter.

        ..  container:: example

            Gets storage format of ``7/4``:

            >>> meter = abjad.Meter((7, 4))
            >>> print(format(meter))
            abjad.Meter(
                '(7/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'
                )

        Returns string.
        """
        if format_specification in ('', 'storage'):
            return system.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __graph__(self, **keywords):
        """
        Gets Graphviz format of meter.

        ..  container:: example

            Graphs ``7/4``:

            >>> meter = abjad.Meter((7, 4))
            >>> meter_graph = meter.__graph__()
            >>> graph(meter_graph) # doctest: +SKIP

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
        def make_offset_node(
            offset,
            leaf_one=None,
            leaf_two=None,
            is_last=False,
        ):
            if not is_last:
                offset_node = uqbar.graphs.Node(
                    attributes={
                        'shape': 'Mrecord',
                        'style': 'filled',
                        'color': 'white',
                        'fontname': 'Arial bold',
                        'fontcolor': 'white',
                        'fillcolor': 'black',
                        },
                    )
            else:
                offset_node = uqbar.graphs.Node(
                    attributes={
                        'shape': 'Mrecord',
                        },
                    )
            offset_field = uqbar.graphs.RecordField(
                label=str(offset),
                )
            weight_field = uqbar.graphs.RecordField(
                label='+' * offsets[offset],
                )
            group = uqbar.graphs.RecordGroup()
            group.extend([offset_field, weight_field])
            offset_node.append(group)
            offset_subgraph.append(offset_node)
            leaf_one_node = node_mapping[leaf_one]
            edge = uqbar.graphs.Edge(
                attributes={'style': 'dotted'},
                )
            edge.attach(leaf_one_node, offset_node)
            if leaf_two:
                leaf_two_node = node_mapping[leaf_two]
                edge = uqbar.graphs.Edge(
                    attributes={'style': 'dotted'},
                    )
                edge.attach(leaf_two_node, offset_node)
        import abjad
        offsets = abjad.MetricAccentKernel.count_offsets(
            abjad.sequence(self.depthwise_offset_inventory).flatten(depth=-1))
        graph = uqbar.graphs.Graph(
            name='G',
            attributes={
                'bgcolor': 'transparent',
                'fontname': 'Arial',
                'penwidth': 2,
                'truecolor': True,
                },
            edge_attributes={
                'penwidth': 2,
                },
            node_attributes={
                'fontname': 'Arial',
                'fontsize': 12,
                'penwidth': 2,
                },
            )
        node_mapping = {}
        root = self._root_node
        nodes = [root] + list(root.depth_first())
        leaves = [_ for _ in nodes if not hasattr(_, 'children')]
        for node in nodes:
            graphviz_node = uqbar.graphs.Node()
            graphviz_node.attributes['label'] = str(node.preprolated_duration)
            if isinstance(node, abjad.rhythmtrees.RhythmTreeContainer):
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
        offset = leaves[0].start_offset
        offset_subgraph = uqbar.graphs.Graph(
            name='cluster_offsets',
            attributes={
                'style': 'rounded',
                },
            )
        graph.append(offset_subgraph)
        make_offset_node(offset, leaves[0])
        for one, two in abjad.sequence(leaves).nwise():
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
                >>> for x in meter:
                ...    x
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
                if isinstance(child, abjad.rhythmtrees.RhythmTreeLeaf):
                    result.append(child)
                else:
                    result.extend(recurse(child))
            result.append(node)
            return result
        result = recurse(self.root_node)
        for x in result:
            start_offset = mathtools.NonreducedFraction(
                x.start_offset).with_denominator(self.denominator)
            stop_offset = mathtools.NonreducedFraction(
                x.stop_offset).with_denominator(self.denominator)
            yield start_offset, stop_offset

    def __str__(self):
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

        Returns string.
        """
        return '{}/{}'.format(self.numerator, self.denominator)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return system.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.rtm_format],
            storage_format_kwargs_names=[],
            )

    @staticmethod
    def _make_gridded_test_rhythm(grid_length, rhythm_number, denominator=16):
        """
        Make test rhythm number ``rhythm_number`` that fits ``grid_length``.

        Returns selection of one or more possibly tied notes.

        ..  container:: example

            The eight test rhythms that fit a length-``4`` grid:

            >>> for rhythm_number in range(8):
            ...     notes = abjad.Meter._make_gridded_test_rhythm(
            ...         4, rhythm_number, denominator=4)
            ...     measure = abjad.Measure((4, 4), notes)
            ...     print('{}\t{}'.format(rhythm_number, str(measure)))
            ...
            0	Measure((4, 4), "c'1")
            1	Measure((4, 4), "c'2. c'4")
            2	Measure((4, 4), "c'2 c'4 c'4")
            3	Measure((4, 4), "c'2 c'2")
            4	Measure((4, 4), "c'4 c'4 c'2")
            5	Measure((4, 4), "c'4 c'4 c'4 c'4")
            6	Measure((4, 4), "c'4 c'2 c'4")
            7	Measure((4, 4), "c'4 c'2.")

        ..  container:: example

            The sixteenth test rhythms for that a length-``5`` grid:

            >>> for rhythm_number in range(16):
            ...     notes = abjad.Meter._make_gridded_test_rhythm(
            ...         5, rhythm_number, denominator=4)
            ...     measure = abjad.Measure((5, 4), notes)
            ...     print('{}\t{}'.format(rhythm_number, str(measure)))
            ...
            0	Measure((5, 4), "c'1 ~ c'4")
            1	Measure((5, 4), "c'1 c'4")
            2	Measure((5, 4), "c'2. c'4 c'4")
            3	Measure((5, 4), "c'2. c'2")
            4	Measure((5, 4), "c'2 c'4 c'2")
            5	Measure((5, 4), "c'2 c'4 c'4 c'4")
            6	Measure((5, 4), "c'2 c'2 c'4")
            7	Measure((5, 4), "c'2 c'2.")
            8	Measure((5, 4), "c'4 c'4 c'2.")
            9	Measure((5, 4), "c'4 c'4 c'2 c'4")
            10	Measure((5, 4), "c'4 c'4 c'4 c'4 c'4")
            11	Measure((5, 4), "c'4 c'4 c'4 c'2")
            12	Measure((5, 4), "c'4 c'2 c'2")
            13	Measure((5, 4), "c'4 c'2 c'4 c'4")
            14	Measure((5, 4), "c'4 c'2. c'4")
            15	Measure((5, 4), "c'4 c'1")

        Use for testing meter establishment.
        """
        import abjad
        # check input
        assert abjad.mathtools.is_positive_integer(grid_length)
        assert isinstance(rhythm_number, int)
        assert abjad.mathtools.is_positive_integer_power_of_two(denominator)
        # find count of all rhythms that fit grid length
        rhythm_count = 2 ** (grid_length - 1)
        # read rhythm number cyclically to allow large and
        # negative rhythm numbers
        rhythm_number = rhythm_number % rhythm_count
        # find binary representation of rhythm
        binary_representation = abjad.mathtools.integer_to_binary_string(
            rhythm_number)
        binary_representation = binary_representation.zfill(grid_length)
        # partition binary representation of rhythm
        parts = abjad.sequence(binary_representation).group_by()
        # find durations
        durations = [
            abjad.Duration(len(part), denominator)
            for part in parts
            ]
        # make notes
        maker = abjad.NoteMaker()
        notes = maker([0], durations)
        # return notes
        return notes

    @staticmethod
    def _rewrite_meter(
        components,
        meter,
        boundary_depth=None,
        initial_offset=None,
        maximum_dot_count=None,
        rewrite_tuplets=True,
        repeat_ties=False,
    ):
        def recurse(
            boundary_depth=None,
            boundary_offsets=None,
            depth=0,
            logical_tie=None,
        ):
            offsets = abjad.meter._MeterManager.get_offsets_at_depth(
                depth,
                offset_inventory,
                )
            #print('DEPTH:', depth)
            logical_tie_duration = logical_tie._get_preprolated_duration()
            logical_tie_timespan = abjad.inspect(logical_tie).timespan()
            logical_tie_start_offset = logical_tie_timespan.start_offset
            logical_tie_stop_offset = logical_tie_timespan.stop_offset
            logical_tie_starts_in_offsets = logical_tie_start_offset in offsets
            logical_tie_stops_in_offsets = logical_tie_stop_offset in offsets
            if not abjad.meter._MeterManager.is_acceptable_logical_tie(
                logical_tie_duration=logical_tie_duration,
                logical_tie_starts_in_offsets=logical_tie_starts_in_offsets,
                logical_tie_stops_in_offsets=logical_tie_stops_in_offsets,
                maximum_dot_count=maximum_dot_count,
            ):
                #print('UNACCEPTABLE:', logical_tie, logical_tie_start_offset, logical_tie_stop_offset)
                #print('\t', ' '.join([str(x) for x in offsets]))
                split_offset = None
                offsets = abjad.meter._MeterManager.get_offsets_at_depth(
                    depth,
                    offset_inventory,
                    )
                # If the logical tie's start aligns, take the latest possible offset.
                if logical_tie_starts_in_offsets:
                    offsets = reversed(offsets)
                for offset in offsets:
                    if logical_tie_start_offset < offset < logical_tie_stop_offset:
                        split_offset = offset
                        break
                #print('\tABS:', split_offset)
                if split_offset is not None:
                    split_offset -= logical_tie_start_offset
                    #print('\tREL:', split_offset)
                    #print()
                    shards = abjad.mutate(logical_tie[:]).split(
                        [split_offset],
                        repeat_ties=repeat_ties,
                        )
                    logical_ties = [abjad.LogicalTie(_) for _ in shards]
                    for logical_tie in logical_ties:
                        recurse(
                            boundary_depth=boundary_depth,
                            boundary_offsets=boundary_offsets,
                            depth=depth,
                            logical_tie=logical_tie,
                            )
                else:
                    #print()
                    recurse(
                        boundary_depth=boundary_depth,
                        boundary_offsets=boundary_offsets,
                        depth=depth + 1,
                        logical_tie=logical_tie,
                        )
            elif abjad.meter._MeterManager.is_boundary_crossing_logical_tie(
                boundary_depth=boundary_depth,
                boundary_offsets=boundary_offsets,
                logical_tie_start_offset=logical_tie_start_offset,
                logical_tie_stop_offset=logical_tie_stop_offset,
            ):
                #print('BOUNDARY CROSSING', logical_tie, logical_tie_start_offset, logical_tie_stop_offset)
                offsets = boundary_offsets
                if logical_tie_start_offset in boundary_offsets:
                    offsets = reversed(boundary_offsets)
                split_offset = None
                for offset in offsets:
                    if logical_tie_start_offset < offset < logical_tie_stop_offset:
                        split_offset = offset
                        break
                assert split_offset is not None
                #print('\tABS:', split_offset)
                split_offset -= logical_tie_start_offset
                #print('\tREL:', split_offset)
                #print()
                shards = abjad.mutate(logical_tie[:]).split(
                    [split_offset],
                    repeat_ties=repeat_ties,
                    )
                logical_ties = [abjad.LogicalTie(shard) for shard in shards]
                for logical_tie in logical_ties:
                    recurse(
                        boundary_depth=boundary_depth,
                        boundary_offsets=boundary_offsets,
                        depth=depth,
                        logical_tie=logical_tie,
                        )
            else:
                #print('ACCEPTABLE:', logical_tie, logical_tie_start_offset, logical_tie_stop_offset)
                #print('\t', ' '.join([str(x) for x in offsets]))
                #print()
                logical_tie[:]._fuse()
        import abjad
        assert isinstance(components, abjad.Selection), repr(components)
        if not isinstance(meter, abjad.Meter):
            meter = abjad.Meter(meter)
        boundary_depth = boundary_depth or meter.preferred_boundary_depth
        # Validate arguments.
        assert abjad.select(components).are_contiguous_logical_voice()
        if not isinstance(meter, abjad.Meter):
            meter = abjad.Meter(meter)
        if boundary_depth is not None:
            boundary_depth = int(boundary_depth)
        if maximum_dot_count is not None:
            maximum_dot_count = int(maximum_dot_count)
            assert 0 <= maximum_dot_count
        if initial_offset is None:
            initial_offset = abjad.Offset(0)
        initial_offset = abjad.Offset(initial_offset)
        first_start_offset = abjad.inspect(
            components[0]).timespan().start_offset
        last_start_offset = abjad.inspect(
            components[-1]).timespan().start_offset
        difference = last_start_offset - first_start_offset + initial_offset
        assert difference < meter.implied_time_signature.duration
        # Build offset inventory, adjusted for initial offset and prolation.
        first_offset = abjad.inspect(components[0]).timespan().start_offset
        first_offset -= initial_offset
        prolation = abjad.inspect(components[0]).parentage(
            include_self=False).prolation
        offset_inventory = []
        for offsets in meter.depthwise_offset_inventory:
            offsets = [(x * prolation) + first_offset for x in offsets]
            offset_inventory.append(tuple(offsets))
        # Build boundary offset inventory, if applicable.
        if boundary_depth is not None:
            boundary_offsets = offset_inventory[boundary_depth]
        else:
            boundary_offsets = None
        # Cache results of iterator, as we'll be mutating the underlying collection
        iterator = abjad.meter._MeterManager.iterate_rewrite_inputs(components)
        items = tuple(iterator)
        for item in items:
            if isinstance(item, abjad.LogicalTie):
                #print('RECURSING:', item)
                recurse(
                    boundary_depth=boundary_depth,
                    boundary_offsets=boundary_offsets,
                    depth=0,
                    logical_tie=item,
                    )
            elif isinstance(item, abjad.Tuplet) and not rewrite_tuplets:
                pass
            else:
                #print('DESCENDING:', item)
                preprolated_duration = sum(
                    [x._get_preprolated_duration() for x in item]
                    )
                if preprolated_duration.numerator == 1:
                    preprolated_duration = abjad.NonreducedFraction(
                        preprolated_duration)
                    preprolated_duration = preprolated_duration.with_denominator(
                        preprolated_duration.denominator * 4)
                sub_metrical_hierarchy = abjad.Meter(preprolated_duration)
                sub_boundary_depth = 1
                if boundary_depth is None:
                    sub_boundary_depth = None
                Meter._rewrite_meter(
                    item[:],
                    sub_metrical_hierarchy,
                    boundary_depth=sub_boundary_depth,
                    maximum_dot_count=maximum_dot_count,
                    )

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
            >>> for x in abjad.Meter.fit_meters(
            ...     argument, meters):
            ...     print(x.implied_time_signature)
            ...
            4/4
            4/4
            4/4
            4/4

        ..  container:: example

            Matches a series of hypothetical ``5/4`` measures:

            >>> argument = [(0, 4), (3, 4), (5, 4), (10, 4), (15, 4), (20, 4)]
            >>> for x in abjad.Meter.fit_meters(
            ...     argument, meters):
            ...     print(x.implied_time_signature)
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
        import abjad
        session = abjad.meter._MeterFittingSession(
            kernel_denominator=denominator,
            maximum_run_length=maximum_run_length,
            meters=meters,
            offset_counter=argument,
            )
        meters = session()
        return meters

    def generate_offset_kernel_to_denominator(
        self,
        denominator,
        normalize=True,
    ):
        r"""
        Generates a dictionary of all offsets in a meter up
        to ``denominator``.

        Keys are the offsets and the values are the normalized weights of
        those offsets.

        ..  container:: example

            >>> meter = abjad.Meter((4, 4))
            >>> kernel = meter.generate_offset_kernel_to_denominator(8)
            >>> for offset, weight in sorted(kernel.kernel.items()):
            ...     print('{!s}\t{!s}'.format(offset, weight))
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
        import abjad
        assert mathtools.is_positive_integer_power_of_two(
            denominator // self.denominator)
        inventory = list(self.depthwise_offset_inventory)
        old_flag_count = abjad.Duration(1, self.denominator).flag_count
        new_flag_count = abjad.Duration(1, denominator).flag_count
        extra_depth = new_flag_count - old_flag_count
        for _ in range(extra_depth):
            old_offsets = inventory[-1]
            new_offsets = []
            for first, second in abjad.sequence(old_offsets).nwise():
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
                kernel[offset] = abjad.Multiplier(response, total)
        return abjad.MetricAccentKernel(kernel)

    ### PUBLIC PROPERTIES ###

    @property
    def decrease_monotonic(self):
        """
        Is true when meter divides large primes into collections of ``2``
        and ``3`` that decrease monotonically.

        ..  container:: example

            An asymmetric meter with beats arranged greatest to least:

            >>> meter = abjad.Meter(
            ...     (7, 4),
            ...     decrease_monotonic=True,
            ...     )

            >>> meter.decrease_monotonic
            True

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
            ...     decrease_monotonic=False,
            ...     )

            >>> meter.decrease_monotonic
            False

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

        Returns true or false.
        """
        return self._decrease_monotonic

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
            0 (Offset(0, 1), Offset(7, 4))
            1 (Offset(0, 1), Offset(3, 4), Offset(5, 4), Offset(7, 4))
            2 (Offset(0, 1), Offset(1, 4), Offset(1, 2), Offset(3, 4), Offset(1, 1), Offset(5, 4), Offset(3, 2), Offset(7, 4))

        Returns dictionary.
        """
        import abjad
        inventory = []
        all_offsets = set()
        all_offsets.add(abjad.Offset(self.numerator, self.denominator))
        for depth, nodes in sorted(self.root_node._depthwise_inventory.items()):
            for node in nodes:
                all_offsets.add(abjad.Offset(node.start_offset))
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
        import abjad
        return abjad.Duration(self.numerator, self.denominator)

    @property
    def implied_time_signature(self):
        """
        Gets implied time signature of meter.

        ..  container:: example

            >>> abjad.Meter((4, 4)).implied_time_signature
            TimeSignature((4, 4))

        Returns time signature.
        """
        return abjad_indicators.TimeSignature(
            self.root_node.preprolated_duration
            )

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
        if 3 in mathtools.divisors(self.numerator):
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

        Used by ``mutate().rewrite_meter()``.

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
            >>> print(format(meter.root_node))
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


class MeterList(TypedList):
    """
    Meter list.

    ..  container:: example

        >>> meters = abjad.MeterList([
        ...     (3, 4), (5, 16), (7, 8),
        ...     ])

        >>> abjad.f(meters)
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

    def __illustrate__(self, denominator=16, range_=None, scale=None):
        r"""
        Illustrates meters.

        ..  container:: example

            >>> meters = abjad.MeterList([
            ...     (3, 4), (5, 16), (7, 8),
            ...     ])
            >>> abjad.show(meters, scale=0.5) # doctest: +SKIP

            ..  doctest

                >>> lilypond_file = meters.__illustrate__()
                >>> abjad.f(lilypond_file) # doctest: +SKIP
                \version "2.19..."
                \language "english"
                <BLANKLINE>
                \header {
                    tagline = ##f
                }
                <BLANKLINE>
                \layout {}
                <BLANKLINE>
                \paper {}
                <BLANKLINE>
                \markup {
                    \column
                        {
                            \combine
                                \combine
                                    \translate
                                        #'(1.0 . 1)
                                        \sans
                                            \fontsize
                                                #-3
                                                \center-align
                                                    \fraction
                                                        3
                                                        4
                                    \translate
                                        #'(49.38709677419355 . 1)
                                        \sans
                                            \fontsize
                                                #-3
                                                \center-align
                                                    \fraction
                                                        5
                                                        16
                                \translate
                                    #'(69.54838709677419 . 1)
                                    \sans
                                        \fontsize
                                            #-3
                                            \center-align
                                                \fraction
                                                    7
                                                    8
                            \combine
                                \postscript
                                    #"
                                    0.2 setlinewidth
                                    1 0.5 moveto
                                    49.387... 0.5 lineto
                                    stroke
                                    1 1.25 moveto
                                    1 -0.25 lineto
                                    stroke
                                    49.387... 1.25 moveto
                                    49.387... -0.25 lineto
                                    stroke
                                    49.387... 0.5 moveto
                                    69.548... 0.5 lineto
                                    stroke
                                    49.387... 1.25 moveto
                                    49.387... -0.25 lineto
                                    stroke
                                    69.548... 1.25 moveto
                                    69.548... -0.25 lineto
                                    stroke
                                    69.5483... 0.5 moveto
                                    126 0.5 lineto
                                    stroke
                                    69.5483... 1.25 moveto
                                    69.5483... -0.25 lineto
                                    stroke
                                    126 1.25 moveto
                                    126 -0.25 lineto
                                    stroke
                                    "
                                \postscript
                                    #"
                                    1 -2 moveto
                                    0 -6.153... rlineto
                                    stroke
                                    5.0322... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    9.0645... -2 moveto
                                    0 -3.076... rlineto
                                    stroke
                                    13.0967... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    17.129... -2 moveto
                                    0 -4.615... rlineto
                                    stroke
                                    21.161... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    25.193... -2 moveto
                                    0 -3.076... rlineto
                                    stroke
                                    29.225... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    33.258... -2 moveto
                                    0 -4.615... rlineto
                                    stroke
                                    37.290... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    41.322... -2 moveto
                                    0 -3.076... rlineto
                                    stroke
                                    45.354... -2 moveto
                                    0 -1.538... rlineto
                                    stroke
                                    49.387... -2 moveto
                                    0 -6.153... rlineto
                                    stroke
                                    49.387... -2 moveto
                                    0 -10.909... rlineto
                                    stroke
                                    53.419... -2 moveto
                                    0 -3.636... rlineto
                                    stroke
                                    57.451... -2 moveto
                                    0 -3.636... rlineto
                                    stroke
                                    61.483... -2 moveto
                                    0 -7.272... rlineto
                                    stroke
                                    65.516... -2 moveto
                                    0 -3.636... rlineto
                                    stroke
                                    69.548... -2 moveto
                                    0 -10.909... rlineto
                                    stroke
                                    69.548... -2 moveto
                                    0 -5.517... rlineto
                                    stroke
                                    73.580... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    77.612... -2 moveto
                                    0 -2.758... rlineto
                                    stroke
                                    81.645... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    85.677... -2 moveto
                                    0 -2.758... rlineto
                                    stroke
                                    89.709... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    93.741... -2 moveto
                                    0 -4.137... rlineto
                                    stroke
                                    97.774... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    101.806... -2 moveto
                                    0 -2.758... rlineto
                                    stroke
                                    105.838... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    109.870... -2 moveto
                                    0 -4.137... rlineto
                                    stroke
                                    113.903... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    117.935... -2 moveto
                                    0 -2.758... rlineto
                                    stroke
                                    121.967... -2 moveto
                                    0 -1.379... rlineto
                                    stroke
                                    126 -2 moveto
                                    0 -5.517... rlineto
                                    stroke
                                    "
                        }
                    }

        Returns LilyPond file.
        """
        import abjad
        durations = [_.duration for _ in self]
        total_duration = sum(durations)
        offsets = abjad.mathtools.cumulative_sums(durations, start=0)
        timespans = abjad.TimespanList()
        for one, two in abjad.sequence(offsets).nwise():
            timespan = abjad.Timespan(
                start_offset=one,
                stop_offset=two,
                )
            timespans.append(timespan)
        if range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = 0, total_duration
        minimum = float(abjad.Offset(minimum))
        maximum = float(abjad.Offset(maximum))
        if scale is None:
            scale = 1.
        assert 0 < scale
        postscript_scale = 125. / (maximum - minimum)
        postscript_scale *= float(scale)
        postscript_x_offset = (minimum * postscript_scale) - 1
        timespan_markup = timespans._make_timespan_list_markup(
            timespans,
            postscript_x_offset,
            postscript_scale,
            draw_offsets=False,
            )
        ps = abjad.Postscript()
        rational_x_offset = abjad.Offset(0)
        for meter in self:
            kernel_denominator = denominator or meter.denominator
            kernel = abjad.meter.MetricAccentKernel.from_meter(
                meter, kernel_denominator)
            for offset, weight in sorted(kernel.kernel.items()):
                weight = float(weight) * -40
                ps_x_offset = float(rational_x_offset + offset)
                ps_x_offset *= postscript_scale
                ps_x_offset += 1
                ps = ps.moveto(ps_x_offset, -2)
                ps = ps.rlineto(0, weight)
                ps = ps.stroke()
            rational_x_offset += meter.duration
        ps = abjad.Markup.postscript(ps)
        markup_list = abjad.MarkupList([timespan_markup, ps])
        lines_markup = markup_list.combine()
        fraction_markups = []
        for meter, offset in zip(self, offsets):
            numerator, denominator = meter.numerator, meter.denominator
            fraction = abjad.Markup.fraction(numerator, denominator)
            fraction = fraction.center_align().fontsize(-3).sans()
            x_translation = (float(offset) * postscript_scale)
            x_translation -= postscript_x_offset
            fraction = fraction.translate((x_translation, 1))
            fraction_markups.append(fraction)
        fraction_markup = fraction_markups[0]
        for markup in fraction_markups[1:]:
            markup_list = [fraction_markup, markup]
            markup_list = abjad.MarkupList(markup_list)
            fraction_markup = markup_list.combine()
        markup = abjad.Markup.column([fraction_markup, lines_markup])
        return markup.__illustrate__()

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        import abjad
        return abjad.meter.Meter


class MetricAccentKernel(AbjadValueObject):
    """
    Metric accent kernel.

    ..  container:: example

        >>> hierarchy = abjad.Meter((7, 8))
        >>> kernel = hierarchy.generate_offset_kernel_to_denominator(8)
        >>> kernel
        MetricAccentKernel(
            {
                Offset(0, 1): Multiplier(3, 14),
                Offset(1, 8): Multiplier(1, 14),
                Offset(1, 4): Multiplier(1, 14),
                Offset(3, 8): Multiplier(1, 7),
                Offset(1, 2): Multiplier(1, 14),
                Offset(5, 8): Multiplier(1, 7),
                Offset(3, 4): Multiplier(1, 14),
                Offset(7, 8): Multiplier(3, 14),
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

    __slots__ = (
        '_kernel',
        '_offsets',
        )

    ### INITIALIZER ###

    def __init__(self, kernel=None):
        import abjad
        kernel = kernel or {}
        assert isinstance(kernel, dict)
        #assert 1 < len(kernel)
        for key, value in kernel.items():
            assert isinstance(key, abjad.Offset)
            assert isinstance(value, abjad.Multiplier)
        self._kernel = kernel.copy()
        self._offsets = tuple(sorted(self._kernel))

    ### SPECIAL METHODS ###

    def __call__(self, argument):
        """
        Calls metrical accent kernal on ``argument``.

        >>> upper_staff = abjad.Staff("c'8 d'4. e'8 f'4.")
        >>> lower_staff = abjad.Staff(r'\clef bass c4 b,4 a,2')
        >>> score = abjad.Score([upper_staff, lower_staff])

        >>> kernel = abjad.MetricAccentKernel.from_meter((4, 4))
        >>> kernel(score)
        Multiplier(10, 33)

        Returns float.
        """
        import abjad
        offset_count = self.count_offsets(argument)
        response = abjad.Multiplier(0, 1)
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

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return system.FormatSpecification(
            client=self,
            repr_is_indented=True,
            storage_format_args_values=[self.kernel],
            storage_format_kwargs_names=[],
            )

    ### PUBLIC METHODS ###

    @staticmethod
    def count_offsets(argument):
        r"""
        Count offsets in ``argument``.

        ..  container:: example

            >>> upper_staff = abjad.Staff("c'8 d'4. e'8 f'4.")
            >>> lower_staff = abjad.Staff(r'\clef bass c4 b,4 a,2')
            >>> score = abjad.Score([upper_staff, lower_staff])

            ..  docs::

                >>> abjad.f(score)
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
            ...
            (Offset(0, 1), 2)
            (Offset(1, 8), 2)
            (Offset(1, 4), 2)
            (Offset(1, 2), 4)
            (Offset(5, 8), 2)
            (Offset(1, 1), 2)

        ..  container:: example

            >>> a = abjad.Timespan(0, 10)
            >>> b = abjad.Timespan(5, 15)
            >>> c = abjad.Timespan(15, 20)

            >>> counter = MetricAccentKernel.count_offsets((a, b, c))
            >>> for offset, count in sorted(counter.items()):
            ...     offset, count
            ...
            (Offset(0, 1), 1)
            (Offset(5, 1), 1)
            (Offset(10, 1), 1)
            (Offset(15, 1), 2)
            (Offset(20, 1), 1)

        Returns counter.
        """
        from abjad import meter
        return meter.OffsetCounter(argument)

    @staticmethod
    def from_meter(meter, denominator=32, normalize=True):
        """
        Create a metric accent kernel from ``meter``.

        Returns new metric accent kernel.
        """
        import abjad
        if not isinstance(meter, abjad.Meter):
            meter = abjad.Meter(meter)
        return meter.generate_offset_kernel_to_denominator(
            denominator=denominator,
            normalize=normalize,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def duration(self):
        """
        Gets duration.
        """
        import abjad
        return abjad.Duration(self._offsets[-1])

    @property
    def kernel(self):
        """
        The kernel datastructure.

        Returns dict.
        """
        return self._kernel.copy()


class OffsetCounter(TypedCounter):
    """
    Offset counter.

    ..  container:: example

        >>> timespans = abjad.TimespanList([
        ...     abjad.Timespan(0, 16),
        ...     abjad.Timespan(5, 12),
        ...     abjad.Timespan(-2, 8),
        ...     ])
        >>> timespan_operand = abjad.Timespan(6, 10)
        >>> timespans = timespans - timespan_operand
        >>> offset_counter = abjad.OffsetCounter(timespans)

        >>> abjad.f(offset_counter)
        abjad.OffsetCounter(
            {
                abjad.Offset(-2, 1): 1,
                abjad.Offset(0, 1): 1,
                abjad.Offset(5, 1): 1,
                abjad.Offset(6, 1): 3,
                abjad.Offset(10, 1): 2,
                abjad.Offset(12, 1): 1,
                abjad.Offset(16, 1): 1,
                }
            )

        >>> abjad.show(offset_counter, scale=0.5) # doctest: +SKIP

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, items=None):
        import abjad
        TypedCounter.__init__(self, item_class=abjad.Offset)
        if items:
            for item in items:
                try:
                    self[item.start_offset] += 1
                    self[item.stop_offset] += 1
                except Exception:
                    if hasattr(item, '_get_timespan'):
                        self[abjad.inspect(item).timespan().start_offset] += 1
                        self[abjad.inspect(item).timespan().stop_offset] += 1
                    else:
                        offset = abjad.Offset(item)
                        self[offset] += 1

    ### SPECIAL METHODS ###

    def __illustrate__(self, range_=None, scale=None):
        r"""
        Illustrates offset counter.

        ..  container:: example

            >>> timespans = abjad.TimespanList([
            ...     abjad.Timespan(0, 16),
            ...     abjad.Timespan(5, 12),
            ...     abjad.Timespan(-2, 8),
            ...     ])
            >>> timespan_operand = abjad.Timespan(6, 10)
            >>> timespans = timespans - timespan_operand
            >>> offset_counter = abjad.OffsetCounter(timespans)
            >>> abjad.show(offset_counter, scale=0.5) # doctest: +SKIP

        Returns LilyPond file.
        """
        import abjad
        if not self:
            return abjad.Markup.null().__illustrate__()
        if isinstance(range_, abjad.Timespan):
            minimum, maximum = range_.start_offset, range_.stop_offset
        elif range_ is not None:
            minimum, maximum = range_
        else:
            minimum, maximum = min(self), max(self)
        minimum = float(abjad.Offset(minimum))
        maximum = float(abjad.Offset(maximum))
        if scale is None:
            scale = 1.
        assert 0 < scale
        postscript_scale = 150. / (maximum - minimum)
        postscript_scale *= float(scale)
        postscript_x_offset = (minimum * postscript_scale) - 1
        ps = abjad.Postscript()
        ps = ps.setlinewidth(0.2)
        ps = ps.setdash([2, 1])
        for offset, count in sorted(self.items()):
            offset = (float(offset) * postscript_scale)
            offset -= postscript_x_offset
            ps = ps.moveto(offset, -1)
            ps = ps.rlineto(0, (float(count) * -3) + 1)
            ps = ps.stroke()
        markup = abjad.Markup.postscript(ps)
        pieces = [markup]
        for offset in sorted(self):
            offset = abjad.Multiplier(offset)
            numerator, denominator = offset.numerator, offset.denominator
            fraction = abjad.Markup.fraction(numerator, denominator)
            fraction = fraction.center_align().fontsize(-3).sans()
            x_translation = (float(offset) * postscript_scale)
            x_translation -= postscript_x_offset
            fraction = fraction.translate((x_translation, 1))
            pieces.append(fraction)
        markup = abjad.Markup.overlay(pieces)
        return markup.__illustrate__()

    ### PRIVATE PROPERTIES ###

    @property
    def _item_coercer(self):
        import abjad
        return abjad.Offset


class _MeterFittingSession(AbjadValueObject):
    """
    Meter-fitting session.

    Used internally by Meter.fit_meters().
    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_cached_offset_counters',
        '_kernel_denominator',
        '_kernels',
        '_longest_kernel',
        '_maximum_run_length',
        '_meters',
        '_offset_counter',
        '_ordered_offsets',
        )

    KernelScore = collections.namedtuple(
        'KernelScore',
        ('kernel', 'score'),
        )

    ### INITIALIZER ###

    def __init__(
        self,
        kernel_denominator=32,
        maximum_run_length=None,
        meters=None,
        offset_counter=None,
    ):
        import abjad
        self._cached_offset_counters = {}
        if maximum_run_length is not None:
            maximum_run_length = int(maximum_run_length)
            assert 0 < maximum_run_length
        self._maximum_run_length = maximum_run_length
        if offset_counter:
            self._offset_counter = abjad.MetricAccentKernel.count_offsets(
                offset_counter)
        else:
            self._offset_counter = {}
        self._ordered_offsets = tuple(sorted(self.offset_counter))
        meters = meters or ()
        self._meters = tuple(abjad.Meter(_) for _ in meters)
        self._kernel_denominator = abjad.Duration(kernel_denominator)
        self._kernels = {}
        for meter in self._meters:
            kernel = meter.generate_offset_kernel_to_denominator(
                self._kernel_denominator)
            self._kernels[kernel] = meter
        if self.kernels:
            self._longest_kernel = sorted(
                self._kernels,
                key=lambda x: x.duration,
                )[-1]
        else:
            self._longest_kernel = None

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Fits meters.

        Returns meter list.
        """
        import abjad
        selected_kernels = []
        current_offset = abjad.Offset(0)
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
                        self.maximum_run_length and
                        1 < len(kernels) and
                        self.maximum_run_length <= len(selected_kernels)
                    ):
                        last_n_kernels = selected_kernels[-self.maximum_run_length:]
                        if len(set(last_n_kernels)) == 1:
                            if kernel == last_n_kernels[-1]:
                                continue
                    initial_score = kernel(offset_counter)
                    lookahead_score = self._get_lookahead_score(
                        current_offset,
                        kernel,
                        kernels,
                        )
                    score = initial_score + lookahead_score
                    kernel_score = self.KernelScore(
                        kernel=kernel,
                        score=score,
                        )
                    kernel_scores.append(kernel_score)
                kernel_scores.sort(key=lambda kernel_score: kernel_score.score)
                winning_kernel = kernel_scores[-1].kernel
            selected_kernels.append(winning_kernel)
            current_offset += winning_kernel.duration
        selected_meters = (self.kernels[_] for _ in selected_kernels)
        selected_meters = abjad.MeterList(selected_meters)
        return selected_meters

    ### PRIVATE METHODS ###

    def _get_kernels(self, selected_kernels):
        return tuple(self.kernels)

    def _get_lookahead_score(self, current_offset, kernel, kernels):
        lookahead_scores = []
        lookahead_offset = current_offset + kernel.duration
        lookahead_offset_counter = self._get_offset_counter_at(
            lookahead_offset)
        for lookahead_kernel in kernels:
            lookahead_scores.append(
                lookahead_kernel(lookahead_offset_counter)
                )
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


class _MeterManager(system.AbjadObject):
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
        import abjad
        if depth < len(offset_inventory):
            return offset_inventory[depth]
        while len(offset_inventory) <= depth:
            new_offsets = []
            old_offsets = offset_inventory[-1]
            for first, second in abjad.sequence(old_offsets).nwise():
                new_offsets.append(first)
                difference = second - first
                half = (first + second) / 2
                if abjad.Duration(1, 8) < difference:
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
        #print '\tTESTING ACCEPTABILITY'
        if not logical_tie_duration.is_assignable:
            return False
        if (
            maximum_dot_count is not None and
            maximum_dot_count < logical_tie_duration.dot_count
        ):
            return False
        if (
            not logical_tie_starts_in_offsets and
            not logical_tie_stops_in_offsets
        ):
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
        #print '\tTESTING BOUNDARY CROSSINGS'
        if boundary_depth is None:
            return False
        if not any(
            logical_tie_start_offset < x < logical_tie_stop_offset
            for x in boundary_offsets
        ):
            return False
        if (
            logical_tie_start_offset in boundary_offsets and
            logical_tie_stop_offset in boundary_offsets
        ):
            return False
        return True

    @staticmethod
    def iterate_rewrite_inputs(argument):
        r"""
        Iterates topmost masked logical ties, rest groups and containers
        in ``argument``, masked by ``argument``.

        >>> string = "abj: ! 2/4 c'4 d'4 ~ !"
        >>> string += "! 4/4 d'8. r16 r8. e'16 ~ "
        >>> string += "2/3 { e'8 ~ e'8 f'8 ~ } f'4 ~ !"
        >>> string += "! 4/4 f'8 g'8 ~ g'4 a'4 ~ a'8 b'8 ~ !"
        >>> string += "! 2/4 b'4 c''4 !"
        >>> string = string.replace('!', '|')
        >>> staff = abjad.Staff(string)

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                {   % measure
                    \time 2/4
                    c'4
                    d'4
                    ~
                }   % measure
                {   % measure
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
                }   % measure
                {   % measure
                    f'8
                    g'8
                    ~
                    g'4
                    a'4
                    ~
                    a'8
                    b'8
                    ~
                }   % measure
                {   % measure
                    \time 2/4
                    b'4
                    c''4
                }   % measure
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
        Tuplet(Multiplier(2, 3), "e'8 ~ e'8 f'8 ~")
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
        import abjad
        last_tie = None
        current_leaf_group = None
        current_leaf_group_is_silent = False
        for x in argument:
            if isinstance(x, (abjad.Note, abjad.Chord)):
                this_tie = x._get_spanners(abjad.Tie) or None
                if current_leaf_group is None:
                    current_leaf_group = []
                elif (
                    current_leaf_group_is_silent or
                    this_tie is None or
                    last_tie != this_tie
                ):
                    yield abjad.LogicalTie(current_leaf_group)
                    current_leaf_group = []
                current_leaf_group_is_silent = False
                current_leaf_group.append(x)
                last_tie = this_tie
            elif isinstance(x, (abjad.Rest, abjad.Skip)):
                if current_leaf_group is None:
                    current_leaf_group = []
                elif not current_leaf_group_is_silent:
                    yield abjad.LogicalTie(current_leaf_group)
                    current_leaf_group = []
                current_leaf_group_is_silent = True
                current_leaf_group.append(x)
                last_tie = None
            elif isinstance(x, abjad.Container):
                if current_leaf_group is not None:
                    yield abjad.LogicalTie(current_leaf_group)
                    current_leaf_group = None
                    last_tie = None
                yield x

            else:
                message = 'unhandled component: {!r}.'
                message = message.format(x)
                raise Exception(message)
        if current_leaf_group is not None:
            yield abjad.LogicalTie(current_leaf_group)
