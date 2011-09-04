from abjad.tools.componenttools._Component import _Component


def repeat_runs_in_sequence_to_count(sequence, indicators):
    '''.. versionadded:: 1.1

    Repeat subruns in `sequence` according to `indicators`.
    The `indicators` input parameter must be a list of
    zero or more ``(start, length, count)`` triples.
    For every ``(start, length, count)`` indicator in `indicators`,
    the function copies ``sequence[start:start+length]`` and inserts
    ``count`` new copies of ``sequence[start:start+length]`` immediately
    after ``sequence[start:start+length]`` in `sequence`.

    .. note:: The function reads the value of ``count`` in every
        ``(start, length, count)`` triple not as the total number
        of occurrences of ``sequence[start:start+length]`` to appear in `sequence`
        after execution, but rather as the number of new occurrences
        of ``sequence[start:start+length]`` to appear in `sequence` after execution.

    .. note:: The function wraps newly created subruns in tuples.
        That is, this function returns output with one more level of
        nesting than given in input.

    To insert ``10`` count of ``sequence[:2]`` at ``sequence[2:2]``::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.repeat_runs_in_sequence_to_count(range(20), [(0, 2, 10)])
        [0, 1, (0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1),
        2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    To insert ``5`` count of ``sequence[10:12]`` at ``sequence[12:12]`` and then
    insert ``5`` count of ``sequence[:2]`` at ``sequence[2:2]``::

        abjad> sequence = range(20)

    ::

        abjad> sequencetools.repeat_runs_in_sequence_to_count(sequence, [(0, 2, 5), (10, 2, 5)])
        [0, 1, (0, 1, 0, 1, 0, 1, 0, 1, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, (10, 11, 10, 11, 10, 11, 10, 11, 10, 11), 12, 13, 14, 15, 16, 17, 18, 19]

    .. note:: This function wraps around the end of `sequence` whenever \
        ``len(sequence) < start + length``.

    To insert ``2`` count of ``[18, 19, 0, 1]`` at ``sequence[2:2]``::

        abjad> sequencetools.repeat_runs_in_sequence_to_count(sequence, [(18, 4, 2)])
        [0, 1, (18, 19, 0, 1, 18, 19, 0, 1), 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    To insert ``2`` count of ``[18, 19, 0, 1, 2, 3, 4]`` at ``sequence[4:4]``::

        abjad> sequencetools.repeat_runs_in_sequence_to_count(sequence, [(18, 8, 2)])
        [0, 1, 2, 3, 4, 5, (18, 19, 0, 1, 2, 3, 4, 5, 18, 19, 0, 1, 2, 3, 4, 5), 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19]

    .. todo:: Implement an optional `wrap` keyword to specify whether \
        this function should wrap around the ened of `sequence` whenever \
        ``len(sequence) < start + length`` or not.

    .. todo:: Reimplement this function to return a generator.

    Generalizations of this function would include functions to repeat subruns
    in `sequence` to not only a certain count, as implemented here, but to a certain
    length, weight or sum. That is, ``sequencetools.repeat_subruns_to_length()``,
    ``sequencetools.repeat_subruns_to_weight()``  and
    ``sequencetools.repeat_subruns_to_sum()``.

    .. versionchanged:: 2.0
        renamed ``sequencetools.repeat_subruns_to_count()`` to
        ``sequencetools.repeat_runs_in_sequence_to_count()``.
    '''

    assert isinstance(sequence, list)
    assert all([not isinstance(x, _Component) for x in sequence])
    assert isinstance(indicators, list)
    assert all([len(x) == 3 for x in indicators])

    len_l = len(sequence)
    instructions = []

    for start, length, count in indicators:
        new_slice = []
        stop = start + length
        for i in range(start, stop):
            new_slice.append(sequence[i % len_l])
        index = stop % len_l
        instruction = (index, new_slice, count)
        instructions.append(instruction)

    result = sequence[:]

    for index, new_slice, count in reversed(sorted(instructions)):
        insert = []
        for i in range(count):
            #result[index:index] = new_slice
            insert.extend(new_slice)
        insert = tuple(insert)
        result.insert(index, insert)

    return result
