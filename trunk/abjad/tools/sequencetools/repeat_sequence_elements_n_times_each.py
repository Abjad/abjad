from abjad.tools import mathtools
import copy


# TODO: generalize count from a single integer count to a list to read cyclically #
def repeat_sequence_elements_n_times_each(sequence, n):
    '''.. versionadded:: 1.1

    Repeat `sequence` elements `n` times each::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.repeat_sequence_elements_n_times_each((1, -1, 2, -3, 5, -5, 6), 2)
        (1, 1, -1, -1, 2, 2, -3, -3, 5, 5, -5, -5, 6, 6)

    Return newly constructed `sequence` object with copied `sequence` elements.

    .. versionchanged:: 2.0
        renamed ``listtools.repeat_elements_to_count()`` to
        ``sequencetools.repeat_sequence_elements_n_times_each()``.
    '''

    if not mathtools.is_nonnegative_integer(n):
        raise ValueError

    result = []
    for element in sequence:
        for x in range(n):
            result.append(copy.copy(element))
    return type(sequence)(result)
