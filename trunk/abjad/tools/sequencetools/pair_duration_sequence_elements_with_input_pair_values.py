from abjad.tools import mathtools


def pair_duration_sequence_elements_with_input_pair_values(duration_sequence, input_pairs):
    r'''.. versionadded:: 2.10

    Pair `duration_sequence` elements with the values of `input_pairs`::

        >>> duration_sequence = [10, 10, 10, 10]
        >>> input_pairs = [('red', 1), ('orange', 18), ('yellow', 200)]

    ::

        >>> sequencetools.pair_duration_sequence_elements_with_input_pair_values(
        ... duration_sequence, input_pairs)
        [(10, 'red'), (10, 'orange'), (10, 'yellow'), (10, 'yellow')]

    Return a list of ``(element, value)`` output pairs.

    The `input_pairs` argument must be a list of ``(value, duration)`` pairs.

    The basic idea behind the function is model which input pair
    value is in effect at the start of each element in `duration_sequence`.
    '''
    from abjad.tools import sequencetools

    assert sequencetools.all_are_numbers(duration_sequence)
    assert sequencetools.all_are_pairs(input_pairs)

    output_pairs = []
    current_element_start = 0
    current_input_pair_index = 0
    current_input_pair = input_pairs[current_input_pair_index]
    current_input_pair_value = current_input_pair[0]
    current_input_pair_duration = current_input_pair[-1]
    current_input_pair_start = 0 
    current_input_pair_stop = current_input_pair_start + current_input_pair_duration

    for element in duration_sequence:
        while current_input_pair_stop <= current_element_start:
            current_input_pair_index += 1
            current_input_pair = input_pairs[current_input_pair_index]
            current_input_pair_value = current_input_pair[0]
            current_input_pair_duration = current_input_pair[-1]
            current_input_pair_start = current_input_pair_stop
            current_input_pair_stop += current_input_pair_duration
        output_pair = (element, current_input_pair_value)
        output_pairs.append(output_pair)
        current_element_start += element

    return output_pairs
