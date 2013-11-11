# -*- encoding: utf-8 -*-
from abjad.tools.topleveltools import attach


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
    from abjad.tools import marktools
    from abjad.tools import scoretools

    # make treble staff
    treble_staff = scoretools.Staff([])
    treble_staff.name = 'treble'
    clef = marktools.Clef('treble')
    attach(clef, treble_staff)

    # make bass staff
    bass_staff = scoretools.Staff([])
    bass_staff.name = 'bass'
    clef = marktools.Clef('bass')
    attach(clef, bass_staff)

    # make piano staff and score
    piano_staff = scoretools.PianoStaff([treble_staff, bass_staff])
    score = scoretools.Score([])
    score.append(piano_staff)

    # return score, treble staff, bass staff
    return score, treble_staff, bass_staff
