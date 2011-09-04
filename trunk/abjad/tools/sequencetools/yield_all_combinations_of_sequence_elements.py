from abjad.tools import mathtools
import copy


def yield_all_combinations_of_sequence_elements(sequence, min_length = None, max_length = None):
    '''.. versionadded:: 2.0

    Yield all combinations of `sequence` in binary string order::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> list(sequencetools.yield_all_combinations_of_sequence_elements([1, 2, 3, 4]))
        [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [1, 2, 3], [4], [1, 4],
        [2, 4], [1, 2, 4], [3, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]

    Yield all combinations of `sequence` greater than or equal to `min_length`
    in binary string order::

        abjad> list(sequencetools.yield_all_combinations_of_sequence_elements([1, 2, 3, 4], min_length = 3))
        [[1, 2, 3], [1, 2, 4], [1, 3, 4], [2, 3, 4], [1, 2, 3, 4]]

    Yield all combinations of `sequence` less than or equal to `max_length`
    in binary string order::

        abjad> list(sequencetools.yield_all_combinations_of_sequence_elements([1, 2, 3, 4], max_length = 2))
        [[], [1], [2], [1, 2], [3], [1, 3], [2, 3], [4], [1, 4], [2, 4], [3, 4]]

    Yield all combiantions of `sequence` greater than or equal to `min_length` and
    less than or equal to `max_length` in lex order::

        abjad> list(sequencetools.yield_all_combinations_of_sequence_elements([1, 2, 3, 4], min_length = 2, max_length = 2))
        [[1, 2], [1, 3], [2, 3], [1, 4], [2, 4], [3, 4]]

    Return generator of newly created `sequence` objects.

    .. versionchanged:: 2.0
        renamed ``sequencetools.sublists()`` to
        ``sequencetools.yield_all_combinations_of_sequence_elements()``.
    '''

    len_l = len(sequence)
    for i in range(2 ** len_l):
        binary_string = mathtools.integer_to_binary_string(i)
        binary_string = binary_string.zfill(len_l)
        sublist = []
        for j, digit in enumerate(reversed(binary_string)):
            if digit == '1':
                # copy makes the function work with score components #
                # copy also makes the function twice as slow on lists of built-ins #
                #sublist.append(sequence[j])
                sublist.append(copy.copy(sequence[j]))
        yield_sublist = True
        if min_length is not None:
            if len(sublist) < min_length:
                yield_sublist = False
        if max_length is not None:
            if max_length < len(sublist):
                yield_sublist = False
        if yield_sublist:
            # type-checking hack ... but is there a better way? #
            if isinstance(sequence, str):
                yield ''.join(sublist)
            else:
                yield type(sequence)(sublist)
