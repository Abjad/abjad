from abjad.tools import durationtools
from abjad.tools import notetools
from abjad.tools import pitchtools


def make_first_n_notes_in_ascending_diatonic_scale(count, written_duration=durationtools.Duration(1, 8), key_signature=None):
    r'''Construct `count` notes with `written_duration`
    according to `key_signature`::

        >>> from abjad.tools import tonalitytools

    ::

        >>> tonalitytools.make_first_n_notes_in_ascending_diatonic_scale(4)
        [Note("c'8"), Note("d'8"), Note("e'8"), Note("f'8")]

    Allow nonassignable `written_duration`::

        >>> staff = Staff(tonalitytools.make_first_n_notes_in_ascending_diatonic_scale(2, (5, 16)))
        >>> f(staff)
        \new Staff {
            c'4 ~
            c'16
            d'4 ~
            d'16
        }

    .. versionadded:: 2.0
        Optional `key_signature` keyword parameter.

    .. versionchanged:: 2.0
        renamed ``leaftools.make_first_n_notes_in_ascending_diatonic_scale()`` to
        ``tonalitytools.make_first_n_notes_in_ascending_diatonic_scale()``.
    '''

    result = notetools.make_notes([0] * count, [written_duration])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        result, key_signature)
    return result
