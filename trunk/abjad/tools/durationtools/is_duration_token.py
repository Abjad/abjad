from abjad.exceptions import DurationError
from abjad.tools.durationtools.duration_token_to_duration_pair import duration_token_to_duration_pair


def is_duration_token(expr):
    '''.. versionadded:: 2.0

    True when `expr` has the form of an Abjad duration token::

        abjad> from abjad.tools import durationtools

    ::

        abjad> durationtools.is_duration_token('8.')
        True

    Otherwise false::

        abjad> durationtools.is_duration_token('foo')
        False

    Return boolean.
    '''

    try:
        duration_token_to_duration_pair(expr)
        return True
    except (TypeError, ValueError, DurationError):
        return False
