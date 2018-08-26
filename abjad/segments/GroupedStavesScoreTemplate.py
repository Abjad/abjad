from abjad.utilities.OrderedDict import OrderedDict
from .ScoreTemplate import ScoreTemplate


class GroupedStavesScoreTemplate(ScoreTemplate):
    r"""
    Grouped staves score template.

    ..  container:: example

        >>> class_ = abjad.GroupedStavesScoreTemplate
        >>> template = class_(staff_count=4)
        >>> abjad.show(template) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(template.__illustrate__()[abjad.Score], strict=60)
            \context Score = "Grouped_Staves_Score"                     %! GroupedStavesScoreTemplate
            <<                                                          %! GroupedStavesScoreTemplate
                \context StaffGroup = "Grouped_Staves_Staff_Group"      %! GroupedStavesScoreTemplate
                <<                                                      %! GroupedStavesScoreTemplate
                    \context Staff = "Staff_1"                          %! GroupedStavesScoreTemplate
                    {                                                   %! GroupedStavesScoreTemplate
                        \context Voice = "Voice_1"                      %! GroupedStavesScoreTemplate
                        {                                               %! GroupedStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedStavesScoreTemplate
                    }                                                   %! GroupedStavesScoreTemplate
                    \context Staff = "Staff_2"                          %! GroupedStavesScoreTemplate
                    {                                                   %! GroupedStavesScoreTemplate
                        \context Voice = "Voice_2"                      %! GroupedStavesScoreTemplate
                        {                                               %! GroupedStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedStavesScoreTemplate
                    }                                                   %! GroupedStavesScoreTemplate
                    \context Staff = "Staff_3"                          %! GroupedStavesScoreTemplate
                    {                                                   %! GroupedStavesScoreTemplate
                        \context Voice = "Voice_3"                      %! GroupedStavesScoreTemplate
                        {                                               %! GroupedStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedStavesScoreTemplate
                    }                                                   %! GroupedStavesScoreTemplate
                    \context Staff = "Staff_4"                          %! GroupedStavesScoreTemplate
                    {                                                   %! GroupedStavesScoreTemplate
                        \context Voice = "Voice_4"                      %! GroupedStavesScoreTemplate
                        {                                               %! GroupedStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedStavesScoreTemplate
                    }                                                   %! GroupedStavesScoreTemplate
                >>                                                      %! GroupedStavesScoreTemplate
            >>                                                          %! GroupedStavesScoreTemplate

        >>> score = template()
        >>> abjad.f(score, strict=60)
        \context Score = "Grouped_Staves_Score"                     %! GroupedStavesScoreTemplate
        <<                                                          %! GroupedStavesScoreTemplate
            \context StaffGroup = "Grouped_Staves_Staff_Group"      %! GroupedStavesScoreTemplate
            <<                                                      %! GroupedStavesScoreTemplate
                \context Staff = "Staff_1"                          %! GroupedStavesScoreTemplate
                {                                                   %! GroupedStavesScoreTemplate
                    \context Voice = "Voice_1"                      %! GroupedStavesScoreTemplate
                    {                                               %! GroupedStavesScoreTemplate
                    }                                               %! GroupedStavesScoreTemplate
                }                                                   %! GroupedStavesScoreTemplate
                \context Staff = "Staff_2"                          %! GroupedStavesScoreTemplate
                {                                                   %! GroupedStavesScoreTemplate
                    \context Voice = "Voice_2"                      %! GroupedStavesScoreTemplate
                    {                                               %! GroupedStavesScoreTemplate
                    }                                               %! GroupedStavesScoreTemplate
                }                                                   %! GroupedStavesScoreTemplate
                \context Staff = "Staff_3"                          %! GroupedStavesScoreTemplate
                {                                                   %! GroupedStavesScoreTemplate
                    \context Voice = "Voice_3"                      %! GroupedStavesScoreTemplate
                    {                                               %! GroupedStavesScoreTemplate
                    }                                               %! GroupedStavesScoreTemplate
                }                                                   %! GroupedStavesScoreTemplate
                \context Staff = "Staff_4"                          %! GroupedStavesScoreTemplate
                {                                                   %! GroupedStavesScoreTemplate
                    \context Voice = "Voice_4"                      %! GroupedStavesScoreTemplate
                    {                                               %! GroupedStavesScoreTemplate
                    }                                               %! GroupedStavesScoreTemplate
                }                                                   %! GroupedStavesScoreTemplate
            >>                                                      %! GroupedStavesScoreTemplate
        >>                                                          %! GroupedStavesScoreTemplate

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_staff_count',
        )

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        super().__init__()
        self._staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls score template.

        Returns score.
        """
        import abjad
        staves = []
        tag = 'GroupedStavesScoreTemplate'
        for index in range(self.staff_count):
            number = index + 1
            voice = abjad.Voice(
                [],
                name='Voice_{}'.format(number),
                tag=tag,
                )
            staff = abjad.Staff(
                [voice],
                name='Staff_{}'.format(number),
                tag=tag,
                )
            staves.append(staff)
            self.voice_abbreviations['v{}'.format(number)] = voice.name
        staff_group = abjad.StaffGroup(
            staves,
            name='Grouped_Staves_Staff_Group',
            tag=tag,
            )
        score = abjad.Score(
            [staff_group],
            name='Grouped_Staves_Score',
            tag=tag,
            )
        return score

    ### PUBLIC PROPERTIES ###

    @property
    def staff_count(self):
        """
        Gets staff count.

        ..  container::

            >>> class_ = abjad.GroupedStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.staff_count
            4

        """
        return self._staff_count

    @property
    def voice_abbreviations(self):
        """
        Gets context name abbreviations.

        ..  container::

            >>> class_ = abjad.GroupedStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.voice_abbreviations
            OrderedDict([])

        """
        return super().voice_abbreviations
