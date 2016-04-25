# -*- coding: utf-8 -*-


def increase_elements(sequence, addenda, indices=None):
    '''Increases `sequence` cyclically by `addenda`.

    ..  container:: example

        **Example 1a.** Increases range elements by ``10`` and ``-10`` in
        alternation:

        ::

            >>> sequencetools.increase_elements(range(10), [10, -10])
            [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]


        **Example 1b.** Increases list elements by 10 and -10 in alternation:

        ::

            >>> sequencetools.increase_elements(list(range(10)), [10, -10])
            [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

        **Example 1c.** Increases tuple elements by 10 and -10 in alternation:

        ::

            >>> sequencetools.increase_elements(tuple(range(10)), [10, -10])
            [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]

    ..  container:: example

        **Example 2.** Increases pairs of elements by ``0.5`` starting at
        indices 0, 4, 8:

        ::

            >>> sequence = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
            >>> addenda = [0.5, 0.5]
            >>> indices = [0, 4, 8]
            >>> sequencetools.increase_elements(sequence, addenda, indices)
            [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]

    Returns list.
    '''
    from abjad.tools import sequencetools
    sequence = list(sequence)
    if indices is None:
        result = []
        for i, element in enumerate(sequence):
            new = element + addenda[i % len(addenda)]
            result.append(new)
    else:
        # assert no overlaps
        tmp = [tuple(range(i, len(addenda))) for i in indices]
        tmp = sequencetools.flatten_sequence(tmp)
        assert len(tmp) == len(set(tmp))
        result = sequence[:]
        for i in indices:
            for j in range(len(addenda)):
                result[i + j] += addenda[j]
    assert isinstance(result, list)
    return result
