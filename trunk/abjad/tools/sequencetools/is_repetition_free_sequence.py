from abjad.tools.sequencetools.iterate_sequence_pairwise_strict import iterate_sequence_pairwise_strict


def is_repetition_free_sequence(expr):
    '''.. versionadded:: 2.0

    True when `expr` is a sequence and `expr` is repetition free::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.is_repetition_free_sequence([0, 1, 2, 6, 7, 8])
        True

    False when `expr` is a sequence and `expr` is not repetition free::

        abjad> sequencetools.is_repetition_free_sequence([0, 1, 2, 2, 7, 8])
        False

    True when `expr` is an empty sequence::

        abjad> sequencetools.is_repetition_free_sequence([])
        True

    False `expr` is not a sequence::

        abjad> sequencetools.is_repetition_free_sequence(17)
        False

    Return boolean.
    '''

    try:
        for left, right in iterate_sequence_pairwise_strict(expr):
            if left == right:
                return False
        return True

    except TypeError:
        return False
