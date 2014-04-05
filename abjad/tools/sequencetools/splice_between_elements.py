# -*- encoding: utf-8 -*-


def splice_between_elements(
    sequence,
    new_elements,
    overhang=(0, 0),
    ):
    '''Splices copies of `new_elements` between each of the elements
    of `sequence`.

    ::

        >>> sequence = [0, 1, 2, 3, 4]
        >>> new_elements = ['A', 'B']

    ::

        >>> sequencetools.splice_between_elements(sequence, new_elements)
        [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

    Splices copies of `new_elements` between each of the elements of `sequence`
    and after the last element of `sequence`:

    ::

        >>> sequencetools.splice_between_elements(
        ...     sequence, new_elements, overhang=(0, 1))
        [0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']

    Splices copies of `new_elements` before the first element of `sequence` and
    between each of the other elements of `sequence`:

    ::

        >>> sequencetools.splice_between_elements(
        ...     sequence, new_elements, overhang=(1, 0))
        ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4]

    Splices copies of `new_elements` before the first element of `sequence`,
    after the last element of `sequence` and between each of the other
    elements of `sequence`:

    ::

        >>> sequencetools.splice_between_elements(
        ...     sequence, new_elements, overhang=(1, 1))
        ['A', 'B', 0, 'A', 'B', 1, 'A', 'B', 2, 'A', 'B', 3, 'A', 'B', 4, 'A', 'B']

    Returns newly constructed list.
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