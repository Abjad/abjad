def iterate_sequence_cyclically_from_start_to_stop(sequence, start, stop):
    '''.. versionadded:: 1.1

    Iterate `sequence` cyclically from `start` to `stop`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> list(sequencetools.iterate_sequence_cyclically_from_start_to_stop(range(20), 18, 10))
        [18, 19, 0, 1, 2, 3, 4, 5, 6, 7, 8, 9]

    Return generator of references to `sequence` elements.

    .. versionchanged:: 2.0
        renamed ``sequencetools.get_cyclic()`` to
        ``sequencetools.iterate_sequence_cyclically_from_start_to_stop()``.
    '''

    len_sequence = len(sequence)
    cur_index = start
    cyclic_stop = stop % len_sequence
    while True:
        cyclic_cur_index = cur_index % len_sequence
        if cyclic_cur_index == cyclic_stop:
            return
        else:
            yield sequence[cyclic_cur_index]
            cur_index += 1
