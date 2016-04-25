# -*- coding: utf-8 -*-
import collections


def negate_elements(sequence, absolute=False, indices=None, period=None):
    '''Negates `sequence` elements.

    ..  container:: example

        Negates all elements:

        ::

            >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
            >>> sequencetools.negate_elements(sequence)
            [-1, -2, -3, -4, -5, 6, 7, 8, 9, 10]

    ..  container:: example

        Negates elements at indices 0, 1 and 2:

        ::

            >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
            >>> sequencetools.negate_elements(sequence, indices=[0, 1, 2])
            [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    ..  container:: example

        Negates elements at indices congruent to 0, 1 or 2 mod 5:

        ::


            >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
            >>> sequencetools.negate_elements(
            ...     sequence,
            ...     indices=[0, 1, 2],
            ...     period=5,
            ...     )
            [-1, -2, -3, 4, 5, 6, 7, 8, -9, -10]

    ..  container:: example

        Negates the absolute value of all elements:

        ::

            >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
            >>> sequencetools.negate_elements(sequence, absolute=True)
            [-1, -2, -3, -4, -5, -6, -7, -8, -9, -10]

    ..  container:: example

        Negates the absolute value elements at indices 0, 1 and 2:

        ::

            >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
            >>> sequencetools.negate_elements(
            ...     sequence,
            ...     absolute=True,
            ...     indices=[0, 1, 2],
            ...     )
            [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    ..  container:: example

        Negates the absolute value elements at indices congruent to 0, 1 or 2
        mod 5:

        ::

            >>> sequence = [1, 2, 3, 4, 5, -6, -7, -8, -9, -10]
            >>> sequencetools.negate_elements(
            ...     sequence,
            ...     absolute=True,
            ...     indices=[0, 1, 2],
            ...     period=5,
            ...     )
            [-1, -2, -3, 4, 5, -6, -7, -8, -9, -10]

    Returns newly constructed list.
    '''

    indices = indices or range(len(sequence))

    if not isinstance(sequence, collections.Sequence):
        message = 'must be sequence: {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    period = period or len(sequence)

    result = []

    for i, element in enumerate(sequence):
        if (i in indices) or (period and i % period in indices):
            if absolute:
                result.append(-abs(element))
            else:
                result.append(-element)
        else:
            result.append(element)

    return result
