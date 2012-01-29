from abjad.tools.durationtools.is_duration_token import is_duration_token


def all_are_duration_tokens(expr):
    '''.. versionadded:: 2.6

    True when `expr` is a sequence of Abjad duration tokens::

        abjad> from abjad.tools import durationtools

    ::

        abjad> duration_tokens = ['8.', (3, 16), Fraction(3, 16), Duration(3, 16)]

    ::

        abjad> durationtools.all_are_duration_tokens(duration_tokens)
        True

    True when `expr` is an empty sequence::

        abjad> durationtools.all_are_duration_tokens([])
        True

    Otherwise false::

        abjad> durationtools.all_are_durations('foo')
        False

    Return boolean.
    '''

    return all([is_duration_token(x) for x in expr])
