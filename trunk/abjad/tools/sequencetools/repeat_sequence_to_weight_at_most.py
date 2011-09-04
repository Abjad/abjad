from abjad.tools.sequencetools._repeat_sequence_to_weight import _repeat_sequence_to_weight


def repeat_sequence_to_weight_at_most(sequence, weight):
    '''.. versionadded:: 1.1

    Repeat `sequence` to `weight` at most::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.repeat_sequence_to_weight_at_most((5, -5, -5), 23)
        (5, -5, -5, 5)

    Return newly constructed `sequence` object.
    '''

    return _repeat_sequence_to_weight(sequence, weight, remainder = 'less')
