from abjad.tools import datastructuretools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import rhythmtreetools
from abjad.tools import scoretools
from abjad.tools import systemtools
from abjad.tools.abctools import AbjadValueObject


class Meter(AbjadValueObject):
    '''Meter.

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

        >>> parser = abjad.rhythmtreetools.RhythmTreeParser()
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
    '''

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
                            child = rhythmtreetools.RhythmTreeContainer(
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
                                rhythmtreetools.RhythmTreeLeaf(
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
                        grouping = rhythmtreetools.RhythmTreeContainer(
                            preprolated_duration=part * preprolated_duration)
                        if factors:
                            for _ in range(part):
                                child = rhythmtreetools.RhythmTreeContainer(
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
                                    rhythmtreetools.RhythmTreeLeaf(
                                        preprolated_duration=(1, denominator)))
                        node.append(grouping)
            else:
                node.extend([rhythmtreetools.RhythmTreeLeaf(
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

        elif isinstance(argument, (str, rhythmtreetools.RhythmTreeContainer)):
            if isinstance(argument, str):
                parsed = rhythmtreetools.RhythmTreeParser()(argument)
                assert len(parsed) == 1
                root = parsed[0]
            else:
                root = argument
            for node in root.nodes:
                assert node.prolation == 1
            numerator = root.preprolated_duration.numerator
            denominator = root.preprolated_duration.denominator

        elif (
            isinstance(argument, (tuple, scoretools.Measure)) or
            is_fraction_like
            ):
            if isinstance(argument, tuple):
                fraction = mathtools.NonreducedFraction(argument)
            elif isinstance(argument, scoretools.Measure):
                prototype = indicatortools.TimeSignature
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
            root = rhythmtreetools.RhythmTreeContainer(
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
        r'''Is true when `argument` is a meter with an rtm format equal to that of
        this meter. Otherwise false.

        Returns true or false.
        '''
        return super(Meter, self).__eq__(argument)

    def __format__(self, format_specification=''):
        r'''Formats meter.

        ..  container:: example

            Gets storage format of ``7/4``:

            >>> meter = abjad.Meter((7, 4))
            >>> print(format(meter))
            abjad.Meter(
                '(7/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'
                )

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __graph__(self, **keywords):
        r'''Gets Graphviz format of meter.

        ..  container:: example

            Graphs ``7/4``:

            >>> meter = abjad.Meter((7, 4))
            >>> meter_graph = meter.__graph__()
            >>> graph(meter_graph) # doctest: +SKIP

            ..  docs::

                >>> print(str(meter_graph))
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
                    subgraph cluster_cluster_offsets {
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
        '''
        import abjad
        def make_offset_node(
            offset,
            leaf_one=None,
            leaf_two=None,
            is_last=False,
            ):
            if not is_last:
                offset_node = abjad.graphtools.GraphvizNode(
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
                offset_node = abjad.graphtools.GraphvizNode(
                    attributes={
                        'shape': 'Mrecord',
                        },
                    )
            offset_field = abjad.graphtools.GraphvizField(
                label=str(offset),
                )
            weight_field = abjad.graphtools.GraphvizField(
                label='+' * offsets[offset],
                )
            group = abjad.graphtools.GraphvizGroup()
            group.extend([offset_field, weight_field])
            offset_node.append(group)
            offset_subgraph.append(offset_node)
            leaf_one_node = node_mapping[leaf_one]
            edge = abjad.graphtools.GraphvizEdge(
                attributes={'style': 'dotted'},
                )
            edge.attach(leaf_one_node, offset_node)
            if leaf_two:
                leaf_two_node = node_mapping[leaf_two]
                edge = abjad.graphtools.GraphvizEdge(
                    attributes={'style': 'dotted'},
                    )
                edge.attach(leaf_two_node, offset_node)
        offsets = abjad.MetricAccentKernel.count_offsets(
            abjad.sequence(self.depthwise_offset_inventory).flatten(depth=-1))
        graph = abjad.graphtools.GraphvizGraph(
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
        for node in self._root_node.nodes:
            graphviz_node = abjad.graphtools.GraphvizNode()
            graphviz_node.attributes['label'] = str(node.preprolated_duration)
            if isinstance(node, rhythmtreetools.RhythmTreeContainer):
                graphviz_node.attributes['shape'] = 'triangle'
            else:
                graphviz_node.attributes['shape'] = 'box'
            graph.append(graphviz_node)
            node_mapping[node] = graphviz_node
            if node.parent is not None:
                abjad.graphtools.GraphvizEdge().attach(
                    node_mapping[node.parent],
                    node_mapping[node],
                    )
        leaves = self._root_node.leaves
        offset = leaves[0].start_offset
        offset_subgraph = abjad.graphtools.GraphvizSubgraph(
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
        r'''Hashes meter.

        Returns integer.
        '''
        return super(Meter, self).__hash__()

    def __iter__(self):
        r'''Iterates meter.

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
        '''
        def recurse(node):
            result = []
            for child in node:
                if isinstance(child, rhythmtreetools.RhythmTreeLeaf):
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
        r'''Gets string representation of meter.

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
        '''
        return '{}/{}'.format(self.numerator, self.denominator)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.rtm_format],
            storage_format_kwargs_names=[],
            )

    @staticmethod
    def _make_gridded_test_rhythm(grid_length, rhythm_number, denominator=16):
        r'''Make test rhythm number `rhythm_number` that fits `grid_length`.

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
        '''
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
        import abjad
        assert isinstance(components, abjad.Selection), repr(components)
        if not isinstance(meter, abjad.Meter):
            meter = abjad.Meter(meter)
        boundary_depth = boundary_depth or meter.preferred_boundary_depth
        def recurse(
            boundary_depth=None,
            boundary_offsets=None,
            depth=0,
            logical_tie=None,
            ):
            offsets = abjad.MeterManager.get_offsets_at_depth(
                depth,
                offset_inventory,
                )
            #print('DEPTH:', depth)
            logical_tie_duration = logical_tie._get_preprolated_duration()
            logical_tie_timespan = abjad.inspect(logical_tie).get_timespan()
            logical_tie_start_offset = logical_tie_timespan.start_offset
            logical_tie_stop_offset = logical_tie_timespan.stop_offset
            logical_tie_starts_in_offsets = logical_tie_start_offset in offsets
            logical_tie_stops_in_offsets = logical_tie_stop_offset in offsets
            if not abjad.MeterManager.is_acceptable_logical_tie(
                logical_tie_duration=logical_tie_duration,
                logical_tie_starts_in_offsets=logical_tie_starts_in_offsets,
                logical_tie_stops_in_offsets=logical_tie_stops_in_offsets,
                maximum_dot_count=maximum_dot_count,
                ):
                #print('UNACCEPTABLE:', logical_tie, logical_tie_start_offset, logical_tie_stop_offset)
                #print('\t', ' '.join([str(x) for x in offsets]))
                split_offset = None
                offsets = abjad.MeterManager.get_offsets_at_depth(
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
            elif abjad.MeterManager.is_boundary_crossing_logical_tie(
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
            components[0]).get_timespan().start_offset
        last_start_offset = abjad.inspect(
            components[-1]).get_timespan().start_offset
        difference = last_start_offset - first_start_offset + initial_offset
        assert difference < meter.implied_time_signature.duration
        # Build offset inventory, adjusted for initial offset and prolation.
        first_offset = abjad.inspect(components[0]).get_timespan().start_offset
        first_offset -= initial_offset
        prolation = abjad.inspect(components[0]).get_parentage(
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
        iterator = abjad.MeterManager.iterate_rewrite_inputs(components)
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
        r'''Finds the best-matching sequence of meters for the offsets
        contained in `argument`.

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

        Coerces offsets from `argument` via
        `MetricAccentKernel.count_offsets()`.

        Coerces Meters from `meters` via `MeterList`.

        Returns list.
        '''
        import abjad
        session = abjad.metertools.MeterFittingSession(
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
        r'''Generates a dictionary of all offsets in a meter up
        to `denominator`.

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
        '''
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
        r'''Is true when meter divides large primes into collections of ``2``
        and ``3`` that decrease monotonically. Otherwise false.

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
        '''
        return self._decrease_monotonic

    @property
    def denominator(self):
        r'''Gets denominator of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> meter.denominator
            4

        Returns positive integer.
        '''
        return self._denominator

    @property
    def depthwise_offset_inventory(self):
        r'''Gets depthwise offset inventory of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> for depth, offsets in enumerate(
            ...     meter.depthwise_offset_inventory):
            ...     print(depth, offsets)
            0 (Offset(0, 1), Offset(7, 4))
            1 (Offset(0, 1), Offset(3, 4), Offset(5, 4), Offset(7, 4))
            2 (Offset(0, 1), Offset(1, 4), Offset(1, 2), Offset(3, 4), Offset(1, 1), Offset(5, 4), Offset(3, 2), Offset(7, 4))

        Returns dictionary.
        '''
        import abjad
        inventory = []
        all_offsets = set()
        all_offsets.add(abjad.Offset(self.numerator, self.denominator))
        for depth, nodes in sorted(self.root_node.depthwise_inventory.items()):
            for node in nodes:
                all_offsets.add(abjad.Offset(node.start_offset))
            inventory.append(tuple(sorted(all_offsets)))
        return tuple(inventory)

    @property
    def duration(self):
        r'''Gets duration of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> meter.duration
            Duration(7, 4)

        Returns duration.
        '''
        import abjad
        return abjad.Duration(self.numerator, self.denominator)

    @property
    def implied_time_signature(self):
        r'''Gets implied time signature of meter.

        ..  container:: example

            >>> abjad.Meter((4, 4)).implied_time_signature
            TimeSignature((4, 4))

        Returns time signature.
        '''
        return indicatortools.TimeSignature(
            self.root_node.preprolated_duration)

    @property
    def is_compound(self):
        r'''Is true when meter is compound. Otherwise false.

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
        '''
        if 3 in mathtools.divisors(self.numerator):
            if not self.numerator == 3:
                return True
        return False

    @property
    def is_simple(self):
        r'''Is true when meter is simple. Otherwise false.

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
        '''
        return not self.is_compound

    @property
    def numerator(self):
        r'''Gets numerator of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> meter.numerator
            7

        Returns positive integer.
        '''
        return self._numerator

    @property
    def pair(self):
        r'''Gets pair of numerator and denominator of meter.

        ..  container:: example

            >>> meter = abjad.Meter((6, 4))
            >>> meter.pair
            (6, 4)

        Returns pair.
        '''
        return (self.numerator, self.denominator)

    @property
    def preferred_boundary_depth(self):
        r'''Gets preferred boundary depth of meter.

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
        '''
        return self._preferred_boundary_depth

    @property
    def pretty_rtm_format(self):
        r'''Gets pretty RTM format of meter.

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
        '''
        return self.root_node.pretty_rtm_format

    @property
    def root_node(self):
        r'''Gets root node of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> print(format(meter.root_node))
            abjad.rhythmtreetools.RhythmTreeContainer(
                children=(
                    abjad.rhythmtreetools.RhythmTreeContainer(
                        children=(
                            abjad.rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            abjad.rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            abjad.rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            ),
                        preprolated_duration=abjad.NonreducedFraction(3, 4),
                        ),
                    abjad.rhythmtreetools.RhythmTreeContainer(
                        children=(
                            abjad.rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            abjad.rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            ),
                        preprolated_duration=abjad.NonreducedFraction(2, 4),
                        ),
                    abjad.rhythmtreetools.RhythmTreeContainer(
                        children=(
                            abjad.rhythmtreetools.RhythmTreeLeaf(
                                preprolated_duration=abjad.Duration(1, 4),
                                is_pitched=True,
                                ),
                            abjad.rhythmtreetools.RhythmTreeLeaf(
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
        '''
        return self._root_node

    @property
    def rtm_format(self):
        r'''Gets RTM format of meter.

        ..  container:: example

            >>> meter = abjad.Meter((7, 4))
            >>> meter.rtm_format
            '(7/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'

        Returns string.
        '''
        return self._root_node.rtm_format
