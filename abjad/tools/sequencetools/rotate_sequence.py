# -*- coding: utf-8 -*-
import collections


def rotate_sequence(sequence, index=None):
    '''Rotates `sequence`.

    ..  container:: example

        **Example 1.** Rotates `sequence` to the right:

        ::

            >>> sequencetools.rotate_sequence(list(range(10)), 4)
            [6, 7, 8, 9, 0, 1, 2, 3, 4, 5]

    ..  container:: example

        **Example 2.** Rotates `sequence` to the left:

        ::

            >>> sequencetools.rotate_sequence(list(range(10)), -3)
            [3, 4, 5, 6, 7, 8, 9, 0, 1, 2]

    ..  container:: example

        **Example 3.** Rotates `sequence` neither to the right nor the left:

        ::

            >>> sequencetools.rotate_sequence(list(range(10)), 0)
            [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    ..  container:: example

        **Example 4.** Rotates ratio numbers:

        ::

            >>> ratio = mathtools.Ratio((1, 2, 3, 4, 5))
            >>> sequencetools.rotate_sequence(ratio.numbers, 2)
            (4, 5, 1, 2, 3)

    ..  container:: example

        **Example 5.** Rotates interval segment:

        ::

            >>> interval_segment = pitchtools.IntervalSegment((-1, 3, 2, 7))
            >>> sequencetools.rotate_sequence(interval_segment, -1)
            IntervalSegment([3, 2, 7, -1])

    Returns new object of `sequence` type.
    '''
    from abjad.tools import sequencetools
    sequence_type = type(sequence)
    result = sequencetools.Sequence(sequence)
    result = result.rotate(index=index)
    result = sequence_type(result)
    return result
