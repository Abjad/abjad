# -*- coding: utf-8 -*-
import collections
import sys


def replace_elements(
    sequence,
    indices,
    new_material,
    ):
    '''Replaces `sequence` elements.

    ..  container:: example

        **Example 1.** Replaces elements at indices 0, 2, 4, 6 with ``'A'``,
        ``'B'``, ``'C'``, ``'D'``, respectively:

        ::

            >>> sequencetools.replace_elements(
            ...     list(range(16)),
            ...     ([0], 2),
            ...     (['A', 'B', 'C', 'D'], None),
            ...     )
            ['A', 1, 'B', 3, 'C', 5, 'D', 7, 8, 9, 10, 11, 12, 13, 14, 15]

    ..  container:: example

        **Example 2.** Replaces elements at indices 0, 1, 8, 13 with ``'A'``,
        ``'B'``, ``'C'``, ``'D'``, respectively:

        ::

            >>> sequencetools.replace_elements(
            ...     list(range(16)),
            ...     ([0, 1, 8, 13], None),
            ...     (['A', 'B', 'C', 'D'], None),
            ...     )
            ['A', 'B', 2, 3, 4, 5, 6, 7, 'C', 9, 10, 11, 12, 'D', 14, 15]

    ..  container:: example

        **Example 3.** Replaces every element at an even index with ``'*'``:

        ::

            >>> sequencetools.replace_elements(
            ...     list(range(16)),
            ...     ([0], 2),
            ...     (['*'], 1),
            ...     )
            ['*', 1, '*', 3, '*', 5, '*', 7, '*', 9, '*', 11, '*', 13, '*', 15]

    ..  container:: example

        **Example 4.** Replaces every element at an index congruent to 0 (mod
        6) with ``'A'``; replaces every element at an index congruent to 2 (mod
        6) with ``'B'``:

        ::

            >>> sequencetools.replace_elements(
            ...     list(range(16)),
            ...     ([0], 2),
            ...     (['A', 'B'], 3),
            ...     )
            ['A', 1, 'B', 3, 4, 5, 'A', 7, 'B', 9, 10, 11, 'A', 13, 'B', 15]

    Returns new object of `sequence` type.
    '''

    if not isinstance(sequence, collections.Sequence):
        message = 'must by sequence {!r}.'
        message = message.format(sequence)
        raise Exception(message)

    sequence_type = type(sequence)

    assert isinstance(indices, tuple) and len(indices) == 2
    index_values, index_period = indices

    assert isinstance(index_values, list)
    assert isinstance(index_period, (int, type(None)))

    assert isinstance(new_material, tuple) and len(new_material) == 2
    material_values, material_period = new_material

    assert isinstance(material_values, list)
    assert isinstance(material_period, (int, type(None)))

    try:
        maxint = sys.maxint
    except AttributeError:
        maxint = sys.maxsize

    if index_period is None:
        index_period = maxint

    if material_period is None:
        material_period = maxint

    result = []

    material_index = 0

    for index, element in enumerate(sequence):
        if index % index_period in index_values:
            try:
                cyclic_material_index = material_index % material_period
                material_value = material_values[cyclic_material_index]
                result.append(material_value)
            except IndexError:
                result.append(element)
            material_index += 1
        else:
            result.append(element)

    result = sequence_type(result)
    return result
