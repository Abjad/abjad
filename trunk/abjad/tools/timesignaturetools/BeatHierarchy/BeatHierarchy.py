from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import measuretools
from abjad.tools import rhythmtreetools
from abjad.tools.abctools import AbjadObject


class BeatHierarchy(AbjadObject):
    '''.. versionadded:: 2.11

    A rhythm tree-based model of nested time signature groupings.

    The structure of the tree corresponds to the monotonically increasing 
    sequence of factors of the time signature's numerator.

    Each deeper level of the tree divides the previous by the next factor in sequence.

    Prime divisions greater than ``3`` are converted to sequences of ``2`` and ``3``
    summing to that prime. Hence ``5`` becomes ``3+2`` and ``7`` becomes ``3+2+2``.

    The beat hierarchy models many parts of the common practice understanding of meter::

        >>> beat_hierarchy = timesignaturetools.BeatHierarchy((4, 4))

    ::

        >>> beat_hierarchy
        BeatHierarchy((4, 4), big_endian=True)

    ::

        >>> print beat_hierarchy.pretty_rtm_format
        (4/4 (
            (2/4 (
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

    ::

        >>> print timesignaturetools.BeatHierarchy((3, 4)).pretty_rtm_format
        (3/4 (
            1/4
            1/4
            1/4))

    ::

        >>> print timesignaturetools.BeatHierarchy((6, 8)).pretty_rtm_format
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

        >>> print timesignaturetools.BeatHierarchy((5, 4)).pretty_rtm_format
        (5/4 (
            (3/4 (
                1/4
                1/4
                1/4))
            (2/4 (
                1/4
                1/4))))

    ::

        >>> print timesignaturetools.BeatHierarchy((5, 4), big_endian=False).pretty_rtm_format
        (5/4 (
            (2/4 (
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))))

    ::

        >>> print timesignaturetools.BeatHierarchy((12, 8)).pretty_rtm_format
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

    Return beat hierarchy object.
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
        '''Iterate beat hierarchy::

            >>> beat_hierarchy = timesignaturetools.BeatHierarchy((5, 4))

        ::

            >>> for x in beat_hierarchy:
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
        '''True if the beat hierarchy divides large primes into collections of
        ``2`` and ``3`` with big-endian ordering.

        Example 1. Little-endian beat hiearchy::

            >>> beat_hierarchy = timesignaturetools.BeatHierarchy((5, 4), big_endian=False)

        ::

            >>> beat_hierarchy.big_endian
            False

        ::

            >>> print beat_hierarchy.pretty_rtm_format 
            (5/4 (
                (2/4 (
                    1/4
                    1/4))
                (3/4 (
                    1/4
                    1/4
                    1/4))))

        Example 2. Big-endian beat hierarchy::

            >>> beat_hierarchy = timesignaturetools.BeatHierarchy((5, 4), big_endian=True)

        ::

            >>> beat_hierarchy.big_endian
            True

        ::

            >>> print beat_hierarchy.pretty_rtm_format 
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

            >>> beat_hierarchy.denominator
            4

        Return positive integer.
        '''
        return self._denominator

    @property
    def depthwise_offset_inventory(self):
        '''Depthwise inventory of offsets at each grouping level::

            >>> for depth, offsets in beat_hierarchy.depthwise_offset_inventory.items():
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

            >>> beat_hierarchy.duration
            Duration(5, 4)

        Return duration.
        '''
        return durationtools.Duration(self.numerator, self.denominator)

    @property
    def numerator(self):
        r'''Beat hierarchy numerator::

            >>> beat_hierarchy.numerator
            5

        Return positive integer.
        '''
        return self._numerator

    @property
    def pretty_rtm_format(self):
        '''Beat hiearchy pretty RTM format::

            >>> print beat_hierarchy.pretty_rtm_format
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

            >>> beat_hierarchy.root_node
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

            >>> beat_hierarchy.rtm_format
            '(5/4 ((3/4 (1/4 1/4 1/4)) (2/4 (1/4 1/4))))'

        Return string.
        '''
        return self._root_node.rtm_format

    @property
    def storage_format(self):
        '''Beat hierarchy storage format::

            >>> print beat_hierarchy.storage_format
            timesignaturetools.BeatHierarchy(
                (5, 4),
                big_endian=True
                )

        Return string.
        '''
        return AbjadObject.storage_format.fget(self)
