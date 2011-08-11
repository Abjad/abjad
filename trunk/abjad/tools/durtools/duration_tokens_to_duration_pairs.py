from abjad.tools.durtools.duration_token_to_duration_pair import duration_token_to_duration_pair


def duration_tokens_to_duration_pairs(duration_tokens):
    '''.. versionadded:: 2.0

    Change `duration_tokens` to duration pairs::

        abjad> from abjad.tools import durtools

    ::

        abjad> durtools.duration_tokens_to_duration_pairs([Fraction(2, 4), 3, '8.', (5, 16)])
        [(1, 2), (3, 1), (3, 16), (5, 16)]

    Return new object of `duration_tokens` type.
    '''

    return type(duration_tokens)([duration_token_to_duration_pair(x) for x in duration_tokens])

