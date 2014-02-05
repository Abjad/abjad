# -*- encoding: utf-8 -*-


def increase_elements(sequence, addenda, indices=None):
    '''Increases `sequence` cyclically by `addenda`.

    ..  container:: example

        Increases elements cyclically by ``10`` and ``-10`` in alternation:

        ::

            >>> sequencetools.increase_elements(range(10), [10, -10])
            [10, -9, 12, -7, 14, -5, 16, -3, 18, -1]
    
    ..  container:: example

        Increases elements by ``0.5`` at indices 0, 4 and 8 and at one element
        following each:

        ::

            >>> sequence = [1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6]
            >>> sequencetools.increase_elements(
            ...     sequence, [0.5, 0.5], indices=[0, 4, 8])
            [1.5, 1.5, 2, 3, 5.5, 5.5, 1, 2, 5.5, 5.5, 6]

    Returns list.
    '''
    from abjad.tools import sequencetools

    if not isinstance(sequence, (list, tuple)):
        raise TypeError

    if indices is None:
        result = []
        for i, element in enumerate(sequence):
            new = element + addenda[i % len(addenda)]
            result.append(new)
    else:
        # assert no overlaps
        tmp = [range(i, len(addenda)) for i in indices]
        tmp = sequencetools.flatten_sequence(tmp)
        assert len(tmp) == len(set(tmp))
        result = sequence[:]
        for i in indices:
            for j in range(len(addenda)):
                result[i+j] += addenda[j]

    return result
