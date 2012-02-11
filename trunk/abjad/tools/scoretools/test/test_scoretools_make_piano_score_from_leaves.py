from abjad import *
from abjad.tools import iotools


def test_scoretools_make_piano_score_from_leaves_01():
    '''Works with notes.
    '''

    pitches = [-12, 37, -10, 27, 4, 17]
    notes = [Note(x, (1, 4)) for x in pitches]
    score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(notes)

    r"""
    \new Score <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
                r4
                cs''''4
                r4
                ef'''4
                e'4
                f''4
            }
            \context Staff = "bass" {
                \clef "bass"
                c4
                r4
                d4
                r4
                r4
                r4
            }
        >>
    >>
    """

    assert componenttools.is_well_formed_component(score)
    assert score.format == '\\new Score <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t\tr4\n\t\t\tcs\'\'\'\'4\n\t\t\tr4\n\t\t\tef\'\'\'4\n\t\t\te\'4\n\t\t\tf\'\'4\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t\tc4\n\t\t\tr4\n\t\t\td4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t}\n\t>>\n>>'


def test_scoretools_make_piano_score_from_leaves_02():
    '''Works with explicit lowest treble pitch.
    '''

    container = iotools.p("{ g4 a4 b4 c'4 d'4 r4 a4 g4 }")
    container_contents = containertools.eject_contents_of_container(container)
    lowest_treble_pitch = pitchtools.NamedChromaticPitch('a')
    score, treble_staff, bass_staff = scoretools.make_piano_score_from_leaves(
        container_contents, lowest_treble_pitch = lowest_treble_pitch)

    r'''
    \new Score <<
        \new PianoStaff <<
            \context Staff = "treble" {
                \clef "treble"
                r4
                a4
                b4
                c'4
                d'4
                r4
                a4
                r4
            }
            \context Staff = "bass" {
                \clef "bass"
                g4
                r4
                r4
                r4
                r4
                r4
                r4
                g4
            }
        >>
    >>
    '''

    assert score.format == '\\new Score <<\n\t\\new PianoStaff <<\n\t\t\\context Staff = "treble" {\n\t\t\t\\clef "treble"\n\t\t\tr4\n\t\t\ta4\n\t\t\tb4\n\t\t\tc\'4\n\t\t\td\'4\n\t\t\tr4\n\t\t\ta4\n\t\t\tr4\n\t\t}\n\t\t\\context Staff = "bass" {\n\t\t\t\\clef "bass"\n\t\t\tg4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t\tr4\n\t\t\tg4\n\t\t}\n\t>>\n>>'
