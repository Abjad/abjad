# -*- encoding: utf-8 -*-


def remove_repeated_elements(sequence):
    r'''Removed repeated elements from `sequence`.

    ..  container:: example

        ::

            >>> sequence = (17, 18, 18, 18, 19, 20, 21, 22, 22, 24, 24)
            >>> sequencetools.remove_repeated_elements(sequence)
            (17, 18, 19, 20, 21, 22, 24)

    ..  container:: example

        ::

            >>> sequence = [31, 31, 35, 35, 31, 31, 31, 31, 35]
            >>> sequencetools.remove_repeated_elements(sequence)
            [31, 35, 31, 35]

    Returns new object of `sequence` type.
    '''

    if not sequence:
        return type(sequence)()

    result = [sequence[0]]
    for element in sequence[1:]:
        if element != result[-1]:
            result.append(element)

    result = type(sequence)(result)
    return result
