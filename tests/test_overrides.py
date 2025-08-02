import abjad


def test_Tuplet_grob_override_01():
    tuplet = abjad.Tuplet("3:2", "c'8 d'8 e'8 f'8")
    abjad.override(tuplet).Glissando.thickness = 3
    abjad.makers.tweak_tuplet_bracket_edge_height(tuplet)

    assert abjad.lilypond(tuplet) == abjad.string.normalize(
        r"""
        \override Glissando.thickness = 3
        \tweak edge-height #'(0.7 . 0)
        \tuplet 3/2
        {
            c'8
            d'8
            e'8
            f'8
        }
        \revert Glissando.thickness
        """
    )


def test_Container_grob_override_01():
    """
    Noncontext containers bracket grob overrides at opening and closing.
    """

    container = abjad.Container("c'8 d'8 e'8 f'8")
    abjad.override(container).Glissando.thickness = 3

    assert abjad.lilypond(container) == abjad.string.normalize(
        r"""
        {
            \override Glissando.thickness = 3
            c'8
            d'8
            e'8
            f'8
            \revert Glissando.thickness
        }
        """
    )


def test_setting_01():
    r"""
    Works with score metronome mark interface.

    Does not include LilyPond \set command.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    score = abjad.Score([staff])
    abjad.setting(score).tempoWholesPerMinute = r"\musicLength 1*24"

    assert abjad.lilypond(score) == abjad.string.normalize(
        r"""
        \new Score
        \with
        {
            tempoWholesPerMinute = \musicLength 1*24
        }
        <<
            \new Staff
            {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        """
    )


def test_setting_02():
    r"""
    Works with leaf metronome mark interface.

    Includes LilyPond \set command.
    """

    staff = abjad.Staff("c'8 d'8 e'8 f'8")
    score = abjad.Score([staff])
    leaves = abjad.select.leaves(score)
    abjad.setting(leaves[1]).Score.tempoWholesPerMinute = r"\musicLength 1*24"

    assert abjad.lilypond(score) == abjad.string.normalize(
        r"""
        \new Score
        <<
            \new Staff
            {
                c'8
                \set Score.tempoWholesPerMinute = \musicLength 1*24
                d'8
                e'8
                f'8
            }
        >>
        """
    )
