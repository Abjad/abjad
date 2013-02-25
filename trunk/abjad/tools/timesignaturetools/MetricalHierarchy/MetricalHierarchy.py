from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import rhythmtreetools
from abjad.tools import sequencetools
from abjad.tools.abctools import AbjadObject


class MetricalHierarchy(AbjadObject):
    '''.. versionadded:: 2.11

    A rhythm tree-based model of nested time signature groupings.

    The structure of the tree corresponds to the monotonically increasing
    sequence of factors of the time signature's numerator.

    Each deeper level of the tree divides the previous by the next factor in sequence.

    Prime divisions greater than ``3`` are converted to sequences of ``2`` and ``3``
    summing to that prime. Hence ``5`` becomes ``3+2`` and ``7`` becomes ``3+2+2``.

    The metrical hierarchy models many parts of the common practice understanding of meter::

        >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((4, 4))

    ::

        >>> metrical_hierarchy
        MetricalHierarchy('(4/4 (1/4 1/4 1/4 1/4))')

    ::

        >>> print metrical_hierarchy.pretty_rtm_format
        (4/4 (
            1/4
            1/4
            1/4
            1/4))

    ::

        >>> print timesignaturetools.MetricalHierarchy((3, 4)).pretty_rtm_format
        (3/4 (
            1/4
            1/4
            1/4))

    ::

        >>> print timesignaturetools.MetricalHierarchy((6, 8)).pretty_rtm_format
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

        >>> print timesignaturetools.MetricalHierarchy((5, 4)).pretty_rtm_format
        (5/4 (
            (3/4 (
                1/4
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

    ::

        >>> print timesignaturetools.MetricalHierarchy((5, 4),
        ...     decrease_durations_monotonically=False).pretty_rtm_format
        (5/4 (
            (2/4 (
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))))

    ::

        >>> print timesignaturetools.MetricalHierarchy((12, 8)).pretty_rtm_format
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

    Return metrical hierarchy object.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_decrease_durations_monotonically', '_denominator', '_numerator', '_root_node',)

    ### INITIALIZER ###

    def __init__(self, arg, decrease_durations_monotonically=True):

        def recurse(node, factors, denominator, decrease_durations_monotonically):
            if factors:
                factor, factors = factors[0], factors[1:]
                preprolated_duration = node.preprolated_duration / factor
                if factor in (2, 3, 4):
                    if factors:
                        for _ in range(factor):
                            child = rhythmtreetools.RhythmTreeContainer(preprolated_duration=preprolated_duration)
                            node.append(child)
                            recurse(child, factors, denominator, decrease_durations_monotonically)
                    else:
                        for _ in range(factor):
                            node.append(rhythmtreetools.RhythmTreeLeaf(preprolated_duration=(1, denominator)))
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
                        grouping = rhythmtreetools.RhythmTreeContainer(preprolated_duration=part * preprolated_duration)
                        if factors:
                            for _ in range(part):
                                child = rhythmtreetools.RhythmTreeContainer(preprolated_duration=preprolated_duration)
                                grouping.append(child)
                                recurse(child, factors, denominator, decrease_durations_monotonically)
                        else:
                            for _ in range(part):
                                grouping.append(rhythmtreetools.RhythmTreeLeaf(preprolated_duration=(1, denominator)))
                        node.append(grouping)
            else:
                node.extend([rhythmtreetools.RhythmTreeLeaf(preprolated_duration=(1, denominator))
                    for _ in range(node.preprolated_duration.numerator)])

        decrease_durations_monotonically = bool(decrease_durations_monotonically)

        if isinstance(arg, type(self)):
            root = arg.root_node
            numerator, denominator = arg.numerator, arg.denominator
            decrease_durations_monotonically = arg.decrease_durations_monotonically

        elif isinstance(arg, (str, rhythmtreetools.RhythmTreeContainer)):
            if isinstance(arg, str):
                parsed = rhythmtreetools.RhythmTreeParser()(arg)
                assert len(parsed) == 1
                root = parsed[0]
            else:
                root = arg
            for node in root.nodes:
                assert node.prolation == 1
            numerator, denominator = root.preprolated_duration.numerator, root.preprolated_duration.denominator

        elif isinstance(arg, (tuple, measuretools.Measure)) or \
            (hasattr(arg, 'numerator') and hasattr(arg, 'denominator')):
            if isinstance(arg, tuple):
                fraction = mathtools.NonreducedFraction(arg)
            elif isinstance(arg, measuretools.Measure):
                time_signature = contexttools.get_effective_time_signature(arg)
                fraction = mathtools.NonreducedFraction(
                    time_signature.numerator, time_signature.denominator)
            else:
                fraction = mathtools.NonreducedFraction(arg.numerator, arg.denominator)
            numerator, denominator = fraction.numerator, fraction.denominator
            factors = mathtools.factors(numerator)[1:]
            # group two nested levels of 2s into a 4
            if 1 < len(factors) and factors[0] == factors[1] == 2:
                factors[0:2] = [4]
            root = rhythmtreetools.RhythmTreeContainer(preprolated_duration=fraction)
            recurse(root, factors, denominator, decrease_durations_monotonically)

        else:
            raise ValueError("Can't initialize {} from {!r}.".format(type(self).__name__, arg))

        self._root_node = root
        self._numerator = numerator
        self._denominator = denominator
        self._decrease_durations_monotonically = decrease_durations_monotonically

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        if type(self) == type(expr):
            if self.rtm_format == expr.rtm_format:
                return True
        return False

    def __iter__(self):
        '''Iterate metrical hierarchy::

            >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((5, 4))

        ::

            >>> for x in metrical_hierarchy:
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

        Yield pairs.
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

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.rtm_format)

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _keyword_argument_names(self):
        return ()

    @property
    def _positional_argument_values(self):
        return (self.rtm_format,)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def decrease_durations_monotonically(self):
        '''True if the metrical hierarchy divides large primes into collections of
        ``2`` and ``3`` that decrease monotonically.

        Example 1. Metrical hiearchy with durations that increase monotonically::

            >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((5, 4),
            ...     decrease_durations_monotonically=False)

        ::

            >>> metrical_hierarchy.decrease_durations_monotonically
            False

        ::

            >>> print metrical_hierarchy.pretty_rtm_format
            (5/4 (
                (2/4 (
                    1/4
                    1/4))
                (3/4 (
                    1/4
                    1/4
                    1/4))))

        Example 2. Metrical hierarchy with durations that decrease monotonically::

            >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((5, 4),
            ...     decrease_durations_monotonically=True)

        ::

            >>> metrical_hierarchy.decrease_durations_monotonically
            True

        ::

            >>> print metrical_hierarchy.pretty_rtm_format
            (5/4 (
                (3/4 (
                    1/4
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))))

        Return boolean.
        '''
        return self._decrease_durations_monotonically

    @property
    def denominator(self):
        r'''Beat hierarchy denominator::

            >>> metrical_hierarchy.denominator
            4

        Return positive integer.
        '''
        return self._denominator

    @property
    def depthwise_offset_inventory(self):
        '''Depthwise inventory of offsets at each grouping level::

            >>> for depth, offsets in enumerate(metrical_hierarchy.depthwise_offset_inventory):
            ...     print depth, offsets
            0 (Offset(0, 1), Offset(5, 4))
            1 (Offset(0, 1), Offset(3, 4), Offset(5, 4))
            2 (Offset(0, 1), Offset(1, 4), Offset(1, 2), Offset(3, 4), Offset(1, 1), Offset(5, 4))

        Return dictionary.
        '''
        inventory = []
        for depth, nodes in sorted(self.root_node.depthwise_inventory.items()):
            offsets = []
            for node in nodes:
                offsets.append(durationtools.Offset(node.start_offset))
            offsets.append(durationtools.Offset(self.numerator, self.denominator))
            inventory.append(tuple(offsets))
        return tuple(inventory)

    @property
    def preprolated_duration(self):
        '''Beat hierarchy preprolated_duration::

            >>> metrical_hierarchy.preprolated_duration
            Duration(5, 4)

        Return preprolated_duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    @property
    def graphviz_format(self):
        '''Graphviz format of hierarchy's root node:

        ::

            >>> print metrical_hierarchy.graphviz_format
            digraph G {
                node_0 [label="5/4",
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
                node_0 -> node_1;
                node_0 -> node_5;
                node_1 -> node_2;
                node_1 -> node_3;
                node_1 -> node_4;
                node_5 -> node_6;
                node_5 -> node_7;
            }

        ::

            >>> iotools.graph(metrical_hierarchy) # doctest: +SKIP

        Return string.
        '''
        return self.root_node.graphviz_format

    @property
    def implied_time_signature(self):
        '''Implied time signature:

        ::

            >>> timesignaturetools.MetricalHierarchy((4, 4)).implied_time_signature
            TimeSignatureMark((4, 4))

        Return TimeSignatureMark object.
        '''
        return contexttools.TimeSignatureMark(self.root_node.preprolated_duration)

    @property
    def numerator(self):
        r'''Beat hierarchy numerator::

            >>> metrical_hierarchy.numerator
            5

        Return positive integer.
        '''
        return self._numerator

    @property
    def pretty_rtm_format(self):
        '''Beat hiearchy pretty RTM format::

            >>> print metrical_hierarchy.pretty_rtm_format
            (5/4 (
                (3/4 (
                    1/4
                    1/4
                    1/4))
                (2/4 (
                    1/4
                    1/4))))

        Return string.
        '''
        return self.root_node.pretty_rtm_format

    @property
    def root_node(self):
        '''Beat hiearchy root node::

            >>> metrical_hierarchy.root_node
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
                                )
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
                                )
                            ),
                        preprolated_duration=NonreducedFraction(2, 4)
                        )
                    ),
                preprolated_duration=NonreducedFraction(5, 4)
                )

        Return rhythm tree node.
        '''
        return self._root_node

    @property
    def rtm_format(self):
        '''Beat hierarchy RTM format::

            >>> metrical_hierarchy.rtm_format
            '(5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))'

        Return string.
        '''
        return self._root_node.rtm_format

    @property
    def storage_format(self):
        '''Beat hierarchy storage format::

            >>> print metrical_hierarchy.storage_format
            timesignaturetools.MetricalHierarchy(
                '(5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))'
                )

        Return string.
        '''
        return AbjadObject.storage_format.fget(self)

    ### PRIVATE METHODS ###

    def _get_recurser(self):


        return recurse

    ### PUBLIC METHODS ###

    def generate_offset_kernel_to_denominator(self, denominator, normalize=True):
        r'''Generate a dictionary of all offsets in a metrical hierarchy up
        to `denominator`, where the keys are the offsets and the values
        are the normalized weights of those offsets:

        ::

            >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((4, 4))
            >>> kernel = metrical_hierarchy.generate_offset_kernel_to_denominator(8)
            >>> for offset, weight in sorted(kernel.kernel.iteritems()):
            ...     print '{}\t{}'.format(offset, weight)
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
        responds to a given metrical hierarchy.

        Return dictionary.
        '''
        from abjad.tools import timesignaturetools
        assert mathtools.is_positive_integer_power_of_two(
            denominator / self.denominator)

        inventory = list(self.depthwise_offset_inventory)
        old_flag_count = durationtools.Duration(1, self.denominator).flag_count
        new_flag_count = durationtools.Duration(1, denominator).flag_count
        extra_depth = new_flag_count - old_flag_count
        for _ in range(extra_depth):
            old_offsets = inventory[-1]
            new_offsets = []
            for first, second in sequencetools.iterate_sequence_pairwise_strict(old_offsets):
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

        return timesignaturetools.MetricalKernel(kernel)
