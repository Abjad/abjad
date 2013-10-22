# -*- encoding: utf-8 -*-


def make_empty_piano_score():
    r'''Make empty piano score:

    ::

        >>> score, treble, bass = scoretools.make_empty_piano_score()

    ..  doctest::

        >>> f(score)
        \new Score <<
            \new PianoStaff <<
                \context Staff = "treble" {
                    \clef "treble"
                }
                \context Staff = "bass" {
                    \clef "bass"
                }
            >>
        >>

    Returns score, treble staff, bass staff.
    '''
    from abjad.tools import contexttools
    from abjad.tools import stafftools
    from abjad.tools import scoretools

    # make treble staff
    treble_staff = stafftools.Staff([])
    treble_staff.name = 'treble'
    contexttools.ClefMark('treble')(treble_staff)

    # make bass staff
    bass_staff = stafftools.Staff([])
    bass_staff.name = 'bass'
    contexttools.ClefMark('bass')(bass_staff)

    # make piano staff and score
    piano_staff = scoretools.PianoStaff([treble_staff, bass_staff])
    score = scoretools.Score([])
    score.append(piano_staff)

    # return score, treble staff, bass staff
    return score, treble_staff, bass_staff
