from abjad.tools import contexttools
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

        >>> quantizationtools.BeatHierarchy((4, 4))
        BeatHierarchy(TimeSignatureMark((4, 4)), big_endian=True)

    ::

        >>> print quantizationtools.BeatHierarchy((4, 4)).pretty_rtm_format
        (4 (
            (2 (
                1
                1))
            (2 (
                1
                1))))

    ::

        >>> print quantizationtools.BeatHierarchy((3, 4)).pretty_rtm_format
        (3 (
            1
            1
            1))

    ::

        >>> print quantizationtools.BeatHierarchy((6, 8)).pretty_rtm_format
        (6 (
            (3 (
                1
                1
                1))
            (3 (
                1
                1
                1))))

    ::

        >>> print quantizationtools.BeatHierarchy((5, 4)).pretty_rtm_format
        (5 (
            (3 (
                1
                1
                1))
            (2 (
                1
                1))))

    ::

        >>> print quantizationtools.BeatHierarchy((5, 4), big_endian=False).pretty_rtm_format
        (5 (
            (2 (
                1
                1))
            (3 (
                1
                1
                1))))

    ::

        >>> print quantizationtools.BeatHierarchy((12, 8)).pretty_rtm_format
        (12 (
            (6 (
                (3 (
                    1
                    1
                    1))
                (3 (
                    1
                    1
                    1))))
            (6 (
                (3 (
                    1
                    1
                    1))
                (3 (
                    1
                    1
                    1))))))

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
        root = rhythmtreetools.RhythmTreeContainer(numerator)
        
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
                            node.append(rhythmtreetools.RhythmTreeLeaf())

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
                                grouping.append(rhythmtreetools.RhythmTreeLeaf())
                        node.append(grouping)

            else:
                node.extend([rhythmtreetools.RhythmTreeLeaf() for _ in range(node.duration)])

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
        denominator = self.time_signature.denominator
        for x in result:
            yield (x.offset / denominator, (x.offset + x.duration) / denominator)

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def big_endian(self):
        '''True if the beat hierarchy divides large primes into `2s` and `3s` with
        big-endian ordering:

        ::

            >>> bh = quantizationtools.BeatHierarchy((5, 4), big_endian=True)
            >>> bh.big_endian
            True
            >>> print bh.pretty_rtm_format 
            (5 (
                (3 (
                    1
                    1
                    1))
                (2 (
                    1
                    1))))

        ::

            >>> bh = quantizationtools.BeatHierarchy((5, 4), big_endian=False)
            >>> bh.big_endian
            False
            >>> print bh.pretty_rtm_format 
            (5 (
                (2 (
                    1
                    1))
                (3 (
                    1
                    1
                    1))))

        Return boolean.
        '''
        return self._big_endian

    @property
    def pretty_rtm_format(self):
        '''The pretty RTM format of the root RhythmTreeNode of the BeatHierarchy:

        ::

            >>> bh = quantizationtools.BeatHierarchy((2, 4))

        ::

            >>> print bh.root_node.pretty_rtm_format
            (2 (
                1
                1))

        ::

            >>> print bh.pretty_rtm_format
            (2 (
                1
                1))


        Return string.
        '''
        return self.root_node.pretty_rtm_format

    @property
    def root_node(self):
        '''The root `RhythmTreeNode` of the `BeatHierarchy`:

        ::

            >>> quantizationtools.BeatHierarchy((2, 4)).root_node
            RhythmTreeContainer(
                children=(
                    RhythmTreeLeaf(
                        duration=1,
                        is_pitched=True,
                        ),
                    RhythmTreeLeaf(
                        duration=1,
                        is_pitched=True,
                        ),
                ),
                duration=2
                )

        Return `RhythmTreeNode` instance.
        '''
        return self._root_node

    @property
    def rtm_format(self):
        '''The RTM format of the root RhythmTreeNode of the BeatHierarchy:

        ::

            >>> bh = quantizationtools.BeatHierarchy((2, 4))

        ::

            >>> print bh.root_node.rtm_format
            (2 (1 1))

        ::

            >>> print bh.rtm_format
            (2 (1 1))

        Return string.
        '''
        return self._root_node.rtm_format

    @property
    def time_signature(self):
        '''The `TimeSignatureMark` associated with the `BeatHierarchy`: 

        ::

            >>> bh = quantizationtools.BeatHierarchy((7, 4))
            >>> bh.time_signature
            TimeSignatureMark((7, 4))

        Return `TimeSignatureMark` instance.
        '''
        return self._time_signature

