import abjad


# TODO: Move to doctests
def test_custom_score_template_class_01():
    """
    Score template with named contexts.
    """

    class NamedContextScoreTemplate(abjad.ScoreTemplate):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            voice = abjad.Voice(name="Blue_Voice")
            staff = abjad.Staff(name="Red_Staff")
            score = abjad.Score(name="Green_Score")
            staff.append(voice)
            score.append(staff)
            return score

    named_context_score_template = NamedContextScoreTemplate()
    score = named_context_score_template()

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \context Score = "Green_Score"
        <<
            \context Staff = "Red_Staff"
            {
                \context Voice = "Blue_Voice"
                {
                }
            }
        >>
        """
    )


def test_custom_score_template_class_02():
    """
    Score template with custom (voice and staff) contexts.

    CAUTION: always use built-in LilyPond score context; do not rename.
    """

    class CustomContextScoreTemplate(abjad.ScoreTemplate):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            custom_voice = abjad.Voice(lilypond_type="CustomVoice")
            custom_staff = abjad.Staff(lilypond_type="CustomStaff")
            score = abjad.Score()
            custom_staff.append(custom_voice)
            score.append(custom_staff)
            return score

    custom_context_score_template = CustomContextScoreTemplate()
    score = custom_context_score_template()

    assert abjad.lilypond(score) == abjad.String.normalize(
        r"""
        \new Score
        <<
            \new CustomStaff
            {
                \new CustomVoice
                {
                }
            }
        >>
        """
    )
