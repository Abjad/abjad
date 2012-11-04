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
        MetricalHierarchy((4, 4), big_endian=True)

    ::

        >>> print metrical_hierarchy.pretty_rtm_format
        (4/4 (
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

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

        >>> print timesignaturetools.MetricalHierarchy((5, 4), big_endian=False).pretty_rtm_format
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
            (6/8 (
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))))
            (6/8 (
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))))))

    Return metrical hierarchy object.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_big_endian', '_denominator', '_numerator', '_root_node',)

    ### INITIALIZER ###

    def __init__(self, arg, big_endian=True):
        if isinstance(arg, tuple):
            arg = mathtools.NonreducedFraction(arg)
        elif isinstance(arg, measuretools.Measure):
            arg = contexttools.get_effective_time_signature(arg)
        self._numerator, self._denominator = arg.numerator, arg.denominator
        self._big_endian = bool(big_endian)

        factors = mathtools.factors(self.numerator)[1:]
        fraction = mathtools.NonreducedFraction(self.numerator, self.denominator)
        root = rhythmtreetools.RhythmTreeContainer(fraction)
         
        def recurse(node, factors):
            if factors:
                factor, factors = factors[0], factors[1:]
                duration = node.duration / factor

                if factor in (2, 3):
                    if factors:
                        for _ in range(factor):
                            child = rhythmtreetools.RhythmTreeContainer(duration)
                            node.append(child)
                            recurse(child, factors)
                    else:
                        for _ in range(factor):
                            node.append(rhythmtreetools.RhythmTreeLeaf((1, self.denominator)))

                else:
                    parts = [3]
                    total = 3
                    while total < factor:
                        if self.big_endian:
                            parts.append(2)
                        else:
                            parts.insert(0, 2)
                        total += 2
                    for part in parts:
                        grouping = rhythmtreetools.RhythmTreeContainer(part * duration)
                        if factors:
                            for _ in range(part):
                                child = rhythmtreetools.RhythmTreeContainer(duration)
                                grouping.append(child)
                                recurse(child, factors)
                        else:
                            for _ in range(part):
                                grouping.append(rhythmtreetools.RhythmTreeLeaf((1, self.denominator)))
                        node.append(grouping)

            else:
                node.extend([rhythmtreetools.RhythmTreeLeaf((1, self.denominator)) 
                    for _ in range(node.duration.numerator)])

        recurse(root, factors)
        self._root_node = root

    ### SPECIAL METHODS ###

    def __iter__(self):
        '''Iterate metrical hierarchy::

            >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((5, 4))

        ::

            >>> for x in metrical_hierarchy:
            ...    x
            ... 
            (Offset(0, 1), NonreducedFraction(1, 4))
            (NonreducedFraction(1, 4), NonreducedFraction(2, 4))
            (NonreducedFraction(2, 4), NonreducedFraction(3, 4))
            (Offset(0, 1), NonreducedFraction(3, 4))
            (NonreducedFraction(3, 4), NonreducedFraction(4, 4))
            (NonreducedFraction(4, 4), NonreducedFraction(5, 4))
            (NonreducedFraction(3, 4), NonreducedFraction(5, 4))
            (Offset(0, 1), NonreducedFraction(5, 4))

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
            yield x.start_offset, x.stop_offset

    ### READ-ONLY PRIVATE PROPERTIES ###

    @property
    def _mandatory_argument_values(self):
        return ((self.numerator, self.denominator),)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def big_endian(self):
        '''True if the metrical hierarchy divides large primes into collections of
        ``2`` and ``3`` with big-endian ordering.

        Example 1. Little-endian metrical hiearchy::

            >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((5, 4), big_endian=False)

        ::

            >>> metrical_hierarchy.big_endian
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

        Example 2. Big-endian metrical hierarchy::

            >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((5, 4), big_endian=True)

        ::

            >>> metrical_hierarchy.big_endian
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
        return self._big_endian

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

            >>> for depth, offsets in metrical_hierarchy.depthwise_offset_inventory.items():
            ...     print depth, offsets
            0 (Offset(0, 1), Offset(5, 4))
            1 (Offset(0, 1), Offset(3, 4), Offset(5, 4))
            2 (Offset(0, 1), Offset(1, 4), Offset(1, 2), Offset(3, 4), Offset(1, 1), Offset(5, 4))

        Return dictionary.
        '''
        inventory = {}
        for depth, nodes in self.root_node.depthwise_inventory.items():
            offsets = []
            for node in nodes:
                offsets.append(durationtools.Offset(node.start_offset))
            offsets.append(durationtools.Offset(self.numerator, self.denominator))
            inventory[depth] = tuple(offsets)
        return inventory

    @property
    def duration(self):
        '''Beat hierarchy duration::

            >>> metrical_hierarchy.duration
            Duration(5, 4)

        Return duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

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
                                duration=durationtools.Duration(1, 4),
                                is_pitched=True,
                                ),
                            RhythmTreeLeaf(
                                duration=durationtools.Duration(1, 4),
                                is_pitched=True,
                                ),
                            RhythmTreeLeaf(
                                duration=durationtools.Duration(1, 4),
                                is_pitched=True,
                                ),
                        ),
                        duration=NonreducedFraction(3, 4)
                        ),
                    RhythmTreeContainer(
                        children=(
                            RhythmTreeLeaf(
                                duration=durationtools.Duration(1, 4),
                                is_pitched=True,
                                ),
                            RhythmTreeLeaf(
                                duration=durationtools.Duration(1, 4),
                                is_pitched=True,
                                ),
                        ),
                        duration=NonreducedFraction(2, 4)
                        ),
                ),
                duration=NonreducedFraction(5, 4)
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
                (5, 4),
                big_endian=True
                )

        Return string.
        '''
        return AbjadObject.storage_format.fget(self)

    ### PUBLIC METHODS ###

    def generate_offset_kernel_to_denominator(self, denominator):
        r'''Generate a dictionary of all offsets in a metrical hierarchy up
        to `denominator`, where the keys are the offsets and the values
        are the normalized weights of those offsets:
        
        ::
        
            >>> metrical_hierarchy = timesignaturetools.MetricalHierarchy((4, 4))
            >>> kernel = metrical_hierarchy.generate_offset_kernel_to_denominator(8)
            >>> for offset, weight in sorted(kernel.iteritems()):
            ...     print '{}\t{}'.format(offset, weight)
            ...
            0       4/19
            1/8     1/19
            1/4     2/19
            3/8     1/19
            1/2     3/19
            5/8     1/19
            3/4     2/19
            7/8     1/19
            1       4/19
         
        This is useful for testing how strongly a collection of offsets
        responds to a given metrical hierarchy.
        
        Return dictionary.
        '''
        assert mathtools.is_positive_integer_power_of_two(
            denominator / self.denominator)

        inventory = [value for key, value in sorted(self.depthwise_offset_inventory.items())]
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
            
        for offset, response in kernel.iteritems():
            kernel[offset] = durationtools.Multiplier(response, total)
        
        return kernel
