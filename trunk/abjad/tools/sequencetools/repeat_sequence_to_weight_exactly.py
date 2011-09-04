from abjad.tools.sequencetools._repeat_sequence_to_weight import _repeat_sequence_to_weight


def repeat_sequence_to_weight_exactly(sequence, weight):
    '''.. versionadded:: 1.1

    Repeat `sequence` to `weight` exactly::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.repeat_sequence_to_weight_exactly((5, -5, -5), 23)
        (5, -5, -5, 5, -3)

    Return newly constructed `sequence` object.
    '''

    return _repeat_sequence_to_weight(sequence, weight, remainder = 'chop')
