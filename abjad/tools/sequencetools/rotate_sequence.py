# -*- encoding: utf-8 -*-
import copy


def rotate_sequence(sequence, n):
    '''Rotates `sequence`.

    Rotates `sequence` to the right:

    ::

        >>> sequencetools.rotate_sequence(list(range(10)), 4)
        [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

    Rotates `sequence` to the left:

    ::

        >>> sequencetools.rotate_sequence(list(range(10)), -3)
        [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

    Rotates `sequence` neither to the right nor the left:

    ::

        >>> sequencetools.rotate_sequence(list(range(10)), 0)
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    Rotates ratio numbers:

    ::

        >>> ratio = mathtools.Ratio((1, 2, 3, 4, 5))
        >>> sequencetools.rotate_sequence(ratio.numbers, 2)
        (4, 5, 1, 2, 3)

    Rotates interval segment:

    ::

        >>> interval_segment = pitchtools.IntervalSegment((-1, 3, 2, 7))
        >>> sequencetools.rotate_sequence(interval_segment, -1)
        IntervalSegment([3, 2, 7, -1])

    Returns newly created `sequence` object.
    '''
    from abjad.tools import sequencetools
    result = sequencetools.Sequence(*sequence)
    result = result.rotate(n)
    return type(sequence)(result)