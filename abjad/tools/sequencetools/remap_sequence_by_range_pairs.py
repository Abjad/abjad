# -*- encoding: utf-8 -*-


# TODO: remove?
def remap_sequence_by_range_pairs(sequence, range_pairs):
    r'''Remaps `sequence` by `range_pairs`.

    ::

        >>> sequence = [9, 14, 4, 1, 7, 5, 9, 6, 2, 10, 15, 20, 8, 4, 0, 7]
        >>> range_pairs = [
        ...     ((2, 10), (3, 5)),
        ...     ((10, 20), (6, 8)),
        ...     ]
        >>> sequencetools.remap_sequence_by_range_pairs(sequence, range_pairs)
        [4, 7, 5, 1, 5, 3, 4, 4, 3, 7, 8, 7, 3, 5, 0, 5]

    Returns newly created `sequence` object.
    '''
    result = []
    for old_element in sequence:
        new_element = old_element
        for input_range, output_range in range_pairs:
            input_low, input_high = input_range
            if input_low <= old_element <= input_high:
                output_low, output_high = output_range
                output_difference = output_high - output_low
                new_element -= input_low
                new_element %= (output_difference + 1)
                new_element += output_low
        result.append(new_element)
    return type(sequence)(result)
