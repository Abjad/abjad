def reverse_sequence(sequence):
    '''.. versionadded:: 2.0

    Reverse `sequence`::

        abjad> from abjad.tools import sequencetools

    ::

        abjad> sequencetools.reverse_sequence((1, 2, 3, 4, 5))
        (5, 4, 3, 2, 1)

    Return new `sequence` object.
    '''

    return type(sequence)(reversed(sequence))
