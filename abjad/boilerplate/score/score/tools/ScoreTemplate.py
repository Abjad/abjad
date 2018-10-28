import abjad


class ScoreTemplate(abjad.ScoreTemplate):
    """
    Score template.
    """

    def __call__(self) -> abjad.Score:
        """
        Calls score template.
        """
        voice = abjad.Voice(name='Example_Voice')
        staff = abjad.Staff([voice], name='Example_Staff')
        score = abjad.Score([staff], name='Example_Score')
        return score
