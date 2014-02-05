# -*- encoding: utf-8 -*-


def is_repetition_free_sequence(expr):
    '''Is true when `expr` is a sequence and `expr` is repetition free.

    ::

        >>> sequencetools.is_repetition_free_sequence([0, 1, 2, 6, 7, 8])
        True

    False when `expr` is a sequence and `expr` is not repetition free:

    ::

        >>> sequencetools.is_repetition_free_sequence([0, 1, 2, 2, 7, 8])
        False

    Is true when `expr` is an empty sequence:

    ::

        >>> sequencetools.is_repetition_free_sequence([])
        True

    False `expr` is not a sequence:

    ::

        >>> sequencetools.is_repetition_free_sequence(17)
        False

    Returns boolean.
    '''
    from abjad.tools import sequencetools

    try:
        pairs = sequencetools.iterate_sequence_nwise(expr)
        for left, right in pairs:
            if left == right:
                return False
        return True

    except TypeError:
        return False
