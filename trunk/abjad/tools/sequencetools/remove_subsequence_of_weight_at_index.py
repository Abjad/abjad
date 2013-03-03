def remove_subsequence_of_weight_at_index(sequence, weight, index):
    '''.. versionadded:: 1.1

    Remove subsequence of `weight` at `index`::

        >>> sequence = (1, 1, 2, 3, 5, 5, 1, 2, 5, 5, 6)

    ::

        >>> sequencetools.remove_subsequence_of_weight_at_index(sequence, 13, 4)
        (1, 1, 2, 3, 5, 5, 6)

    Return newly constructed `sequence` object.
    '''

    result = list(sequence[:index])
    total = 0
    for element in sequence[index:]:
        if weight <= total:
            result.append(element)
        elif weight < total + element:
            result.append(total + element - weight)
        total += element
    return type(sequence)(result)
