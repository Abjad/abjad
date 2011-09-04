def splice_new_elements_between_sequence_elements(sequence, new_elements, overhang = (0, 0)):
    '''.. versionadded:: 1.1

    Splice copies of `new_elements` between each of the elements of `sequence`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequence = [0, 1, 2, 3, 4]
        abjad> new_elements = ['A', 'B']

    ::

        abjad> sequencetools.splice_new_elements_between_sequence_elements(sequence, new_elements)
        [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

    Splice copies of `new_elements` between each of the elements of `sequence` and after
    the last element of `sequence`::

        abjad> sequencetools.splice_new_elements_between_sequence_elements(sequence, new_elements, overhang = (0, 1))
        [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']

    Splice copies of `new_elements` before the first element of `sequence` and
    between each of the other elements of `sequence`::

        abjad> sequencetools.splice_new_elements_between_sequence_elements(sequence, new_elements, overhang = (1, 0))
        ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

    Splice copies of `new_elements` before the first element of `sequence`,
    after the last element of `sequence` and between each of the other elements of `sequence`::

        abjad> sequencetools.splice_new_elements_between_sequence_elements(sequence, new_elements, overhang = (1, 1))
        ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']

    Return newly constructed list.

    .. versionchanged:: 2.0
        renamed ``sequencetools.insert_slice_cyclic()`` to
        ``sequencetools.splice_new_elements_between_sequence_elements()``.
    '''

    result = []

    if overhang[0] == 1:
        result.extend(new_elements[:])

    for element in sequence[:-1]:
        result.append(element)
        result.extend(new_elements[:])

    result.append(sequence[-1])

    if overhang[-1] == 1:
        result.extend(new_elements)

    return result
