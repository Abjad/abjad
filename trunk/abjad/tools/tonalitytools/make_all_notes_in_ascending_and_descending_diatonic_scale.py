from abjad.tools import componenttools
from abjad.tools import contexttools
from abjad.tools import durationtools
from abjad.tools import schemetools
from abjad.tools import scoretools
from abjad.tools import stafftools



def make_all_notes_in_ascending_and_descending_diatonic_scale(key_signature=None):
    r'''.. versionadded:: 2.0

    Construct one up-down period of scale according to `key_signature`::

        >>> from abjad.tools import tonalitytools

    ::

        >>> score = tonalitytools.make_all_notes_in_ascending_and_descending_diatonic_scale(
        ... contexttools.KeySignatureMark('E', 'major'))

    ::

        >>> f(score)
        \new Score \with {
            tempoWholesPerMinute = #(ly:make-moment 30 1)
        } <<
            \new Staff {
                \key e \major
                e'8
                fs'8
                gs'8
                a'8
                b'8
                cs''8
                ds''8
                e''8
                ds''8
                cs''8
                b'8
                a'8
                gs'8
                fs'8
                e'4
            }
        >>

    .. versionchanged:: 2.0
        renamed ``construct.scale_period()`` to
        ``tonalitytools.make_all_notes_in_ascending_and_descending_diatonic_scale()``.
    '''
    from abjad.tools import tonalitytools

    ascending_notes = tonalitytools.make_first_n_notes_in_ascending_diatonic_scale(
        8, durationtools.Duration(1, 8), key_signature)
    descending_notes = componenttools.copy_components_and_remove_spanners(ascending_notes[:-1])
    descending_notes.reverse()
    notes = ascending_notes + descending_notes
    notes[-1].written_duration = durationtools.Duration(1, 4)
    staff = stafftools.Staff(notes)
    contexttools.KeySignatureMark(key_signature.tonic, key_signature.mode)(staff)
    score = scoretools.Score([staff])
    score.set.tempo_wholes_per_minute = schemetools.SchemeMoment(30)

    return score
