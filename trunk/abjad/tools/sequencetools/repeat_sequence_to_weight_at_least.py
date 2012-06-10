from abjad.tools.sequencetools._repeat_sequence_to_weight import _repeat_sequence_to_weight


def repeat_sequence_to_weight_at_least(sequence, weight):
    '''.. versionadded:: 1.1

    Repeat `sequence` to `weight` at least::

        >>> from abjad.tools import sequencetools

    ::

        >>> sequencetools.repeat_sequence_to_weight_at_least((5, -5, -5), 23)
        (5, -5, -5, 5, -5)

    Return newly constructed `sequence` object.
    '''

    return _repeat_sequence_to_weight(sequence, weight, remainder='more')
