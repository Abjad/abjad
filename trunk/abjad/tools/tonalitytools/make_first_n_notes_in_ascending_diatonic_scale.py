from abjad.tools import durationtools
from abjad.tools import notetools
from abjad.tools import pitchtools


def make_first_n_notes_in_ascending_diatonic_scale(count, written_duration=None, key_signature=None):
    r'''Make first `count` notes in ascending diatonic scale according to `key_signature`.
    Set `written_duration` equal to `written_duration` or ``1/8``:

    ::

        >>> notes = tonalitytools.make_first_n_notes_in_ascending_diatonic_scale(8)
        >>> staff = Staff(notes)

    ::
    
        >>> f(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'8
            a'8
            b'8
            c''8
        }

    ::
        
        >>> show(staff) # doctest: +SKIP

    Allow nonassignable `written_duration`:

    ::

        >>> notes = tonalitytools.make_first_n_notes_in_ascending_diatonic_scale(
        ...     4, Duration(5, 16))
        >>> staff = Staff(notes)
        >>> time_signature = contexttools.TimeSignatureMark((5, 4))(staff)

    ::

        >>> f(staff)
        \new Staff {
            \time 5/4
            c'4 ~
            c'16
            d'4 ~
            d'16
            e'4 ~
            e'16
            f'4 ~
            f'16
        }

    ::

        >>> show(staff) # doctest: +SKIP

    Return list of notes.
    '''

    # make notes
    written_duration = written_duration or durationtools.Duration(1, 8)
    result = notetools.make_notes([0] * count, [written_duration])
    pitchtools.set_ascending_named_diatonic_pitches_on_tie_chains_in_expr(
        result, key_signature)

    # return notes
    return result
