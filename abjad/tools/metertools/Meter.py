# -*- encoding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import durationtools
from abjad.tools import indicatortools
from abjad.tools import mathtools
from abjad.tools import rhythmtreetools
from abjad.tools import scoretools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class Meter(AbjadObject):
    '''A rhythm tree-based model of nested time signature groupings.

    The structure of the tree corresponds to the monotonically increasing
    sequence of factors of the time signature's numerator.

    Each deeper level of the tree divides the previous by the next factor in
    sequence.

    Prime divisions greater than ``3`` are converted to sequences of ``2`` and
    ``3`` summing to that prime.  Hence ``5`` becomes ``3+2`` and ``7`` becomes
    ``3+2+2``.

    The meter models many parts of the common practice understanding of meter:

    ::

        >>> meter = metertools.Meter((4, 4))

    ::

        >>> meter
        Meter('(4/4 (1/4 1/4 1/4 1/4))')

    ::

        >>> print meter.pretty_rtm_format
        (4/4 (
            1/4
            1/4
            1/4
            1/4))

    ::

        >>> meter = metertools.Meter((3, 4))
        >>> print meter.pretty_rtm_format
        (3/4 (
            1/4
            1/4
            1/4))

    ::

        >>> meter = metertools.Meter((6, 8))
        >>> print meter.pretty_rtm_format
        (6/8 (
            (3/8 (
                1/8
                1/8
                1/8))
            (3/8 (
                1/8
                1/8
                1/8))))

    ::

        >>> meter = metertools.Meter((7, 4))
        >>> print meter.pretty_rtm_format
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

    ::

        >>> meter = metertools.Meter(
        ...     (7, 4), decrease_durations_monotonically=False)
        >>> print meter.pretty_rtm_format
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

    ::

        >>> meter = metertools.Meter((12, 8))
        >>> print meter.pretty_rtm_format
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

    Returns meter object.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_decrease_durations_monotonically',
        '_denominator',
        '_numerator',
        '_root_node',
        )

    ### INITIALIZER ###

    def __init__(self, arg=None, decrease_durations_monotonically=True):

        arg = arg or (4, 4)

        def recurse(
            node, factors, denominator, decrease_durations_monotonically):
            if factors:
                factor, factors = factors[0], factors[1:]
                preprolated_duration = node.preprolated_duration / factor
                if factor in (2, 3, 4, 5):
                    if factors:
                        for _ in range(factor):
                            child = rhythmtreetools.RhythmTreeContainer(
                                preprolated_duration=preprolated_duration)
                            node.append(child)
                            recurse(
                                child,
                                factors,
                                denominator,
                                decrease_durations_monotonically,
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
                        if decrease_durations_monotonically:
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
                                    decrease_durations_monotonically,
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

        decrease_durations_monotonically = \
            bool(decrease_durations_monotonically)

        if isinstance(arg, type(self)):
            root = arg.root_node
            numerator, denominator = arg.numerator, arg.denominator
            decrease_durations_monotonically = \
                arg.decrease_durations_monotonically

        elif isinstance(arg, (str, rhythmtreetools.RhythmTreeContainer)):
            if isinstance(arg, str):
                parsed = rhythmtreetools.RhythmTreeParser()(arg)
                assert len(parsed) == 1
                root = parsed[0]
            else:
                root = arg
            for node in root.nodes:
                assert node.prolation == 1
            numerator = root.preprolated_duration.numerator
            denominator = root.preprolated_duration.denominator

        elif isinstance(arg, (tuple, scoretools.Measure)) or \
            (hasattr(arg, 'numerator') and hasattr(arg, 'denominator')):
            if isinstance(arg, tuple):
                fraction = mathtools.NonreducedFraction(arg)
            elif isinstance(arg, scoretools.Measure):
                time_signature = arg._get_effective(
                    indicatortools.TimeSignature)
                fraction = mathtools.NonreducedFraction(
                    time_signature.numerator, time_signature.denominator)
            else:
                fraction = mathtools.NonreducedFraction(
                    arg.numerator, arg.denominator)
            numerator, denominator = fraction.numerator, fraction.denominator
            factors = mathtools.factors(numerator)[1:]
            # group two nested levels of 2s into a 4
            if 1 < len(factors) and factors[0] == factors[1] == 2:
                factors[0:2] = [4]
            root = rhythmtreetools.RhythmTreeContainer(
                preprolated_duration=fraction)
            recurse(
                root,
                factors,
                denominator,
                decrease_durations_monotonically,
                )

        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, arg)
            raise ValueError(message)

        self._root_node = root
        self._numerator = numerator
        self._denominator = denominator
        self._decrease_durations_monotonically = \
            decrease_durations_monotonically

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a meter with an rtm format equal to that of
        this meter. Otherwise false.

        Returns boolean.
        '''
        if type(self) == type(expr):
            if self.rtm_format == expr.rtm_format:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats meter.

        Set `format_specification` to `''` or `'storage'`.
        Interprets `''` equal to `'storage'`.

            >>> meter = metertools.Meter((7, 4))
            >>> print format(meter)
            metertools.Meter(
                '(7/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'
                )

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'storage'):
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __hash__(self):
        r'''Hashes meter.
        '''
        return hash((type(self), self.rtm_format))

    def __iter__(self):
        r'''Iterates meter.

        ::

            >>> meter = metertools.Meter((5, 4))

        ::

            >>> for x in meter:
            ...    x
            ...
            (NonreducedFraction(0, 4), NonreducedFraction(1, 4))
            (NonreducedFraction(1, 4), NonreducedFraction(2, 4))
            (NonreducedFraction(2, 4), NonreducedFraction(3, 4))
            (NonreducedFraction(3, 4), NonreducedFraction(4, 4))
            (NonreducedFraction(4, 4), NonreducedFraction(5, 4))
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
            start_offset = mathtools.NonreducedFraction(x.start_offset
                ).with_denominator(self.denominator)
            stop_offset = mathtools.NonreducedFraction(x.stop_offset
                ).with_denominator(self.denominator)
            yield start_offset, stop_offset

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            keyword_argument_names=(),
            positional_argument_values=(
                self.rtm_format,
                ),
            )

    ### PUBLIC PROPERTIES ###

    @property
    def decrease_durations_monotonically(self):
        r'''True if the meter divides large primes into collections of ``2``
        and ``3`` that decrease monotonically.

        ..  container:: example

            **Example 1.** Metrical hiearchy with durations that increase
            monotonically:

            ::

                >>> meter = metertools.Meter(
                ...     (7, 4),
                ...     decrease_durations_monotonically=False,
                ...     )

            ::

                >>> meter.decrease_durations_monotonically
                False

            ::

                >>> print meter.pretty_rtm_format
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

        ..  container:: example

            **Example 2.** Meter with durations that
            decrease monotonically:

            ::

                >>> meter = \
                ...     metertools.Meter((7, 4),
                ...     decrease_durations_monotonically=True)

            ::

                >>> meter.decrease_durations_monotonically
                True

            ::

                >>> print meter.pretty_rtm_format
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

        Returns boolean.
        '''
        return self._decrease_durations_monotonically

    @property
    def denominator(self):
        r'''Beat hierarchy denominator:

        ::

            >>> meter.denominator
            4

        Returns positive integer.
        '''
        return self._denominator

    @property
    def depthwise_offset_inventory(self):
        r'''Depthwise inventory of offsets at each grouping level:

        ::

            >>> for depth, offsets in enumerate(
            ...     meter.depthwise_offset_inventory):
            ...     print depth, offsets
            0 (Offset(0, 1), Offset(7, 4))
            1 (Offset(0, 1), Offset(3, 4), Offset(5, 4), Offset(7, 4))
            2 (Offset(0, 1), Offset(1, 4), Offset(1, 2), Offset(3, 4), Offset(1, 1), Offset(5, 4), Offset(3, 2), Offset(7, 4))

        Returns dictionary.
        '''
        inventory = []
        for depth, nodes in sorted(
            self.root_node.depthwise_inventory.items()):
            offsets = []
            for node in nodes:
                offsets.append(durationtools.Offset(node.start_offset))
            offsets.append(
                durationtools.Offset(self.numerator, self.denominator))
            inventory.append(tuple(offsets))
        return tuple(inventory)

    @property
    def graphviz_format(self):
        r'''Graphviz format of hierarchy's root node:

        ::

            >>> print meter.graphviz_format
            digraph G {
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
                node_0 -> node_1;
                node_0 -> node_5;
                node_0 -> node_8;
                node_1 -> node_2;
                node_1 -> node_3;
                node_1 -> node_4;
                node_5 -> node_6;
                node_5 -> node_7;
                node_8 -> node_10;
                node_8 -> node_9;
            }

        ::

            >>> topleveltools.graph(meter) # doctest: +SKIP

        Returns string.
        '''
        return self.root_node.graphviz_format

    @property
    def implied_time_signature(self):
        r'''Implied time signature:

        ::

            >>> metertools.Meter((4, 4)).implied_time_signature
            TimeSignature((4, 4))

        Returns TimeSignature object.
        '''
        return indicatortools.TimeSignature(
            self.root_node.preprolated_duration)

    @property
    def numerator(self):
        r'''Beat hierarchy numerator:

        ::

            >>> meter.numerator
            7

        Returns positive integer.
        '''
        return self._numerator

    @property
    def preprolated_duration(self):
        r'''Beat hierarchy preprolated_duration:

        ::

            >>> meter.preprolated_duration
            Duration(7, 4)

        Returns preprolated_duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    @property
    def pretty_rtm_format(self):
        r'''Beat hiearchy pretty RTM format:

        ::

            >>> print meter.pretty_rtm_format
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
        r'''Beat hiearchy root node:

        ::

            >>> meter.root_node
            RhythmTreeContainer(
                children=(
                    RhythmTreeContainer(
                        children=(
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            ),
                        preprolated_duration=NonreducedFraction(3, 4)
                        ),
                    RhythmTreeContainer(
                        children=(
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            ),
                        preprolated_duration=NonreducedFraction(2, 4)
                        ),
                    RhythmTreeContainer(
                        children=(
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            RhythmTreeLeaf(
                                preprolated_duration=Duration(1, 4),
                                is_pitched=True
                                ),
                            ),
                        preprolated_duration=NonreducedFraction(2, 4)
                        ),
                    ),
                preprolated_duration=NonreducedFraction(7, 4)
                )

        Returns rhythm tree node.
        '''
        return self._root_node

    @property
    def rtm_format(self):
        r'''Beat hierarchy RTM format:

        ::

            >>> meter.rtm_format
            '(7/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4)) (2/4 (1/4 1/4))))'

        Returns string.
        '''
        return self._root_node.rtm_format

    ### PRIVATE METHODS ###

    def _get_recurser(self):
        return recurse

    @staticmethod
    def _make_gridded_test_rhythm(grid_length, rhythm_number, denominator=16):
        r'''Make test rhythm number `rhythm_number` that fits `grid_length`.

        Returns selection of one or more possibly tied notes.

        ..  container:: example

            **Example 1.** The eight test rhythms that fit a length-``4``
            grid:

            ::

                >>> from abjad.tools.metertools import Meter
                >>> for rhythm_number in range(8):
                ...     notes = Meter._make_gridded_test_rhythm(
                ...         4, rhythm_number, denominator=4)
                ...     measure = Measure((4, 4), notes)
                ...     print '{}\t{}'.format(rhythm_number, str(measure))
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

            **Example 2.** The sixteenth test rhythms for that a length-``5``
            grid:

            ::

                >>> for rhythm_number in range(16):
                ...     notes = Meter._make_gridded_test_rhythm(
                ...         5, rhythm_number, denominator=4)
                ...     measure = Measure((5, 4), notes)
                ...     print '{}\t{}'.format(rhythm_number, str(measure))
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
        from abjad.tools import scoretools
        # check input
        assert mathtools.is_positive_integer(grid_length)
        assert isinstance(rhythm_number, int)
        assert mathtools.is_positive_integer_power_of_two(denominator)
        # find count of all rhythms that fit grid length
        rhythm_count = 2 ** (grid_length - 1)
        # read rhythm number cyclically to allow large and
        # negative rhythm numbers
        rhythm_number = rhythm_number % rhythm_count
        # find binary representation of rhythm
        binary_representation = \
            mathtools.integer_to_binary_string(rhythm_number)
        binary_representation = binary_representation.zfill(grid_length)
        # partition binary representation of rhythm
        parts = sequencetools.partition_sequence_by_value_of_elements(
            binary_representation)
        # find durations
        durations = [
            durationtools.Duration(len(part), denominator)
            for part in parts
            ]
        # make notes
        notes = scoretools.make_notes([0], durations)
        # return notes
        return notes

    ### PUBLIC METHODS ###

    @staticmethod
    def fit_meters_to_expr(
        expr,
        meters,
        denominator=32,
        discard_final_orphan_downbeat=True,
        maximum_repetitions=None,
        starting_offset=None,
        ):
        r'''Find the best-matching sequence of meters for the offsets
        contained in `expr`.

        ::

            >>> meters = [metertools.Meter(x)
            ...     for x in [(3, 4), (4, 4), (5, 4)]
            ...     ]

        ..  container:: example

            **Example 1.** Matching a series of hypothetical 4/4 measures:

            ::

                >>> expr = [(0, 4), (4, 4), (8, 4), (12, 4), (16, 4)]
                >>> for x in metertools.Meter.fit_meters_to_expr(
                ...     expr, meters):
                ...     print x.implied_time_signature
                ...
                4/4
                4/4
                4/4
                4/4

        ..  container:: example

            **Example 2.** Matching a series of hypothetical 5/4 measures:

            ::

                >>> expr = [(0, 4), (3, 4), (5, 4), (10, 4), (15, 4), (20, 4)]
                >>> for x in metertools.Meter.fit_meters_to_expr(
                ...     expr, meters):
                ...     print x.implied_time_signature
                ...
                3/4
                3/4
                4/4
                5/4
                5/4

        Offsets are coerced from `expr` via
        `MetricAccentKernel.count_offsets_in_expr()`.

        MetricalHierarchies are coerced from `meters` via
        `MetricalHierarchyInventory`.

        Returns list.
        '''
        from abjad.tools import metertools
        offset_counter = \
            metertools.MetricAccentKernel.count_offsets_in_expr(expr)
        ordered_offsets = sorted(offset_counter, reverse=True)
        if not ordered_offsets:
            return []
        if starting_offset is None:
            start_offset = durationtools.Offset(0)
        else:
            start_offset = durationtools.Offset(starting_offset)
        meter_inventory = datastructuretools.TypedTuple(
            items=meters,
            item_class=metertools.Meter,
            )
        longest_hierarchy = sorted(meter_inventory,
            key=lambda x: x.preprolated_duration, reverse=True)[0]
        longest_kernel_duration = max(
            x.preprolated_duration for x in meter_inventory)
        kernels = [x.generate_offset_kernel_to_denominator(denominator)
            for x in meter_inventory]
        current_start_offset = start_offset
        selected_hierarchies = []
        while len(ordered_offsets) and \
            ordered_offsets[-1] < current_start_offset:
            ordered_offsets.pop()
        while len(ordered_offsets) and \
            current_start_offset <= ordered_offsets[-1]:
            if len(ordered_offsets) == 1:
                if discard_final_orphan_downbeat:
                    if ordered_offsets[0] == current_start_offset:
                        break
            current_stop_offset = \
                current_start_offset + longest_kernel_duration
            current_offset_counter = {}
            for offset in reversed(ordered_offsets):
                if current_start_offset <= offset <= current_stop_offset:
                    current_offset_counter[offset - current_start_offset] = \
                        offset_counter[offset]
                else:
                    break
            if not current_offset_counter:
                winner = longest_hierarchy
            else:
                candidates = []
                if maximum_repetitions is not None:
                    fencepost = -1 * abs(maximum_repetitions)
                    meter_buffer = selected_hierarchies[fencepost:]
                for meter_index, kernel in enumerate(kernels):
                    if maximum_repetitions is not None and \
                        len(meter_buffer) == maximum_repetitions:
                        meter_set = set(meter_buffer +
                            [meter_inventory[meter_index]])
                        if len(meter_set) == 1 and 1 < len(meter_inventory):
                            continue
                    response = kernel(current_offset_counter)
                    candidates.append((response, meter_index))
                candidates.sort(key=lambda x: x[0], reverse=True)
                response, index = candidates[0]
                winner = meter_inventory[index]
            selected_hierarchies.append(winner)
            current_start_offset += winner.preprolated_duration
            while len(ordered_offsets) \
                and ordered_offsets[-1] < current_start_offset:
                ordered_offsets.pop()
        return selected_hierarchies

    def generate_offset_kernel_to_denominator(
        self,
        denominator,
        normalize=True,
        ):
        r'''Generate a dictionary of all offsets in a meter up
        to `denominator`, where the keys are the offsets and the values
        are the normalized weights of those offsets:

        ::

            >>> meter = \
            ...     metertools.Meter((4, 4))
            >>> kernel = \
            ...     meter.generate_offset_kernel_to_denominator(8)
            >>> for offset, weight in sorted(kernel.kernel.iteritems()):
            ...     print '{!s}\t{!s}'.format(offset, weight)
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
        from abjad.tools import metertools
        assert mathtools.is_positive_integer_power_of_two(
            denominator / self.denominator)

        inventory = list(self.depthwise_offset_inventory)
        old_flag_count = durationtools.Duration(1, self.denominator).flag_count
        new_flag_count = durationtools.Duration(1, denominator).flag_count
        extra_depth = new_flag_count - old_flag_count
        for _ in range(extra_depth):
            old_offsets = inventory[-1]
            new_offsets = []
            for first, second in \
                sequencetools.iterate_sequence_nwise(old_offsets):
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
            for offset, response in kernel.iteritems():
                kernel[offset] = durationtools.Multiplier(response, total)

        return metertools.MetricAccentKernel(kernel)
