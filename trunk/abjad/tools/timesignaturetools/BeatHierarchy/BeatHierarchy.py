from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import mathtools
from abjad.tools import rhythmtreetools
from abjad.tools.abctools import AbjadObject


class BeatHierarchy(AbjadObject):
    '''A RhythmTree-based model of the nested groupings within a given time
    signature.

    The structure of the tree corresponds to the monotonically increasing 
    sequence of factors of the time signature's numerator, with each deeper
    level of the tree dividing the previous by the next factor in the sequence.

    Prime divisions greater than `3` are converted to sequences of `2s` and `3s`
    summing to that prime, hence `5` becomes `3+2`, and `7` becomes `3+2+2`.

    This process creates a reasonable analog to the common practice model of
    metrical structure.

    ::

        >>> from experimental import *

    ::

        >>> timesignaturetools.BeatHierarchy((4, 4))
        BeatHierarchy(TimeSignatureMark((4, 4)), big_endian=True)

    ::

        >>> print timesignaturetools.BeatHierarchy((4, 4)).pretty_rtm_format
        (1 (
            (1/2 (
                1/4
                1/4))
            (1/2 (
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
        (3/4 (
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
            (1/2 (
                1/4
                1/4))))

    ::

        >>> print timesignaturetools.BeatHierarchy((5, 4), big_endian=False).pretty_rtm_format
        (5/4 (
            (1/2 (
                1/4
                1/4))
            (3/4 (
                1/4
                1/4
                1/4))))

    ::

        >>> print timesignaturetools.BeatHierarchy((12, 8)).pretty_rtm_format
        (3/2 (
            (3/4 (
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))))
            (3/4 (
                (3/8 (
                    1/8
                    1/8
                    1/8))
                (3/8 (
                    1/8
                    1/8
                    1/8))))))

    Return `BeatHierarchy` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ('_big_endian', '_root_node', '_time_signature')

    ### INITIALIZER ###

    def __init__(self, time_signature, big_endian=True):

        time_signature = contexttools.TimeSignatureMark(time_signature)
        self._time_signature = time_signature

        self._big_endian = bool(big_endian)

        numerator, denominator = time_signature.numerator, time_signature.denominator
        factors = mathtools.factors(numerator)[1:]
        root = rhythmtreetools.RhythmTreeContainer((numerator, denominator))
        
        def recurse(node, factors):
            if factors:
                factor, factors = factors[0], factors[1:]
                duration = durationtools.Duration(node.duration / factor)

                if factor in (2, 3):
                    if factors:
                        for _ in range(factor):
                            child = rhythmtreetools.RhythmTreeContainer(duration)
                            node.append(child)
                            recurse(child, factors)
                    else:
                        for _ in range(factor):
                            node.append(rhythmtreetools.RhythmTreeLeaf((1, denominator)))

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
                                grouping.append(rhythmtreetools.RhythmTreeLeaf((1, denominator)))
                        node.append(grouping)

            else:
                node.extend([rhythmtreetools.RhythmTreeLeaf((1, denominator)) 
                    for _ in range(node.duration.numerator)])

        recurse(root, factors)
        self._root_node = root

    ### SPECIAL METHODS ###

    def __iter__(self):
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

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def big_endian(self):
        '''True if the beat hierarchy divides large primes into `2s` and `3s` with
        big-endian ordering:

        ::

            >>> bh = timesignaturetools.BeatHierarchy((5, 4), big_endian=True)
            >>> bh.big_endian
            True
            >>> print bh.pretty_rtm_format 
            (5/4 (
                (3/4 (
                    1/4
                    1/4
                    1/4))
                (1/2 (
                    1/4
                    1/4))))

        ::

            >>> bh = timesignaturetools.BeatHierarchy((5, 4), big_endian=False)
            >>> bh.big_endian
            False
            >>> print bh.pretty_rtm_format 
            (5/4 (
                (1/2 (
                    1/4
                    1/4))
                (3/4 (
                    1/4
                    1/4
                    1/4))))

        Return boolean.
        '''
        return self._big_endian

    @property
    def depthwise_offset_inventory(self):
        '''Depthwise inventory of offsets at each grouping level:

        ::

            >>> bh = timesignaturetools.BeatHierarchy((5, 4))
            >>> for depth, offsets in bh.depthwise_offset_inventory.items():
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
                offsets.append(node.start_offset)
            offsets.append(durationtools.Offset(self.time_signature.duration))
            inventory[depth] = tuple(offsets)
        return inventory

    @property
    def pretty_rtm_format(self):
        '''The pretty RTM format of the root RhythmTreeNode of the BeatHierarchy:

        ::

            >>> bh = timesignaturetools.BeatHierarchy((2, 4))

        ::

            >>> print bh.root_node.pretty_rtm_format
            (1/2 (
                1/4
                1/4))

        ::

            >>> print bh.pretty_rtm_format
            (1/2 (
                1/4
                1/4))


        Return string.
        '''
        return self.root_node.pretty_rtm_format

    @property
    def root_node(self):
        '''The root `RhythmTreeNode` of the `BeatHierarchy`:

        ::

            >>> timesignaturetools.BeatHierarchy((2, 4)).root_node
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
                duration=Duration(1, 2)
                )

        Return `RhythmTreeNode` instance.
        '''
        return self._root_node

    @property
    def rtm_format(self):
        '''The RTM format of the root RhythmTreeNode of the BeatHierarchy:

        ::

            >>> bh = timesignaturetools.BeatHierarchy((2, 4))

        ::

            >>> print bh.root_node.rtm_format
            (1/2 (1/4 1/4))

        ::

            >>> print bh.rtm_format
            (1/2 (1/4 1/4))

        Return string.
        '''
        return self._root_node.rtm_format

    @property
    def time_signature(self):
        '''The `TimeSignatureMark` associated with the `BeatHierarchy`: 

        ::

            >>> bh = timesignaturetools.BeatHierarchy((7, 4))
            >>> bh.time_signature
            TimeSignatureMark((7, 4))

        Return `TimeSignatureMark` instance.
        '''
        return self._time_signature

    ### PUBLIC METHODS ###

