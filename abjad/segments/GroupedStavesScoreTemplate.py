from abjad.system.Tag import Tag

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
            \context Score = "Grouped_Staves_Score"                     %! abjad.GroupedStavesScoreTemplate.__call__()
            <<                                                          %! abjad.GroupedStavesScoreTemplate.__call__()
                \context StaffGroup = "Grouped_Staves_Staff_Group"      %! abjad.GroupedStavesScoreTemplate.__call__()
                <<                                                      %! abjad.GroupedStavesScoreTemplate.__call__()
                    \context Staff = "Staff_1"                          %! abjad.GroupedStavesScoreTemplate.__call__()
                    {                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                        \context Voice = "Voice_1"                      %! abjad.GroupedStavesScoreTemplate.__call__()
                        {                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                            s1                                          %! abjad.ScoreTemplate.__illustrate__()
                        }                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                    }                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                    \context Staff = "Staff_2"                          %! abjad.GroupedStavesScoreTemplate.__call__()
                    {                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                        \context Voice = "Voice_2"                      %! abjad.GroupedStavesScoreTemplate.__call__()
                        {                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                            s1                                          %! abjad.ScoreTemplate.__illustrate__()
                        }                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                    }                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                    \context Staff = "Staff_3"                          %! abjad.GroupedStavesScoreTemplate.__call__()
                    {                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                        \context Voice = "Voice_3"                      %! abjad.GroupedStavesScoreTemplate.__call__()
                        {                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                            s1                                          %! abjad.ScoreTemplate.__illustrate__()
                        }                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                    }                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                    \context Staff = "Staff_4"                          %! abjad.GroupedStavesScoreTemplate.__call__()
                    {                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                        \context Voice = "Voice_4"                      %! abjad.GroupedStavesScoreTemplate.__call__()
                        {                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                            s1                                          %! abjad.ScoreTemplate.__illustrate__()
                        }                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                    }                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                >>                                                      %! abjad.GroupedStavesScoreTemplate.__call__()
            >>                                                          %! abjad.GroupedStavesScoreTemplate.__call__()

        >>> score = template()
        >>> abjad.f(score, strict=60)
        \context Score = "Grouped_Staves_Score"                     %! abjad.GroupedStavesScoreTemplate.__call__()
        <<                                                          %! abjad.GroupedStavesScoreTemplate.__call__()
            \context StaffGroup = "Grouped_Staves_Staff_Group"      %! abjad.GroupedStavesScoreTemplate.__call__()
            <<                                                      %! abjad.GroupedStavesScoreTemplate.__call__()
                \context Staff = "Staff_1"                          %! abjad.GroupedStavesScoreTemplate.__call__()
                {                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                    \context Voice = "Voice_1"                      %! abjad.GroupedStavesScoreTemplate.__call__()
                    {                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                    }                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                }                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                \context Staff = "Staff_2"                          %! abjad.GroupedStavesScoreTemplate.__call__()
                {                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                    \context Voice = "Voice_2"                      %! abjad.GroupedStavesScoreTemplate.__call__()
                    {                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                    }                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                }                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                \context Staff = "Staff_3"                          %! abjad.GroupedStavesScoreTemplate.__call__()
                {                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                    \context Voice = "Voice_3"                      %! abjad.GroupedStavesScoreTemplate.__call__()
                    {                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                    }                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                }                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                \context Staff = "Staff_4"                          %! abjad.GroupedStavesScoreTemplate.__call__()
                {                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
                    \context Voice = "Voice_4"                      %! abjad.GroupedStavesScoreTemplate.__call__()
                    {                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                    }                                               %! abjad.GroupedStavesScoreTemplate.__call__()
                }                                                   %! abjad.GroupedStavesScoreTemplate.__call__()
            >>                                                      %! abjad.GroupedStavesScoreTemplate.__call__()
        >>                                                          %! abjad.GroupedStavesScoreTemplate.__call__()

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_staff_count",)

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
        site = "abjad.GroupedStavesScoreTemplate.__call__()"
        tag = Tag(site)
        for index in range(self.staff_count):
            number = index + 1
            voice = abjad.Voice([], name="Voice_{}".format(number), tag=tag)
            staff = abjad.Staff([voice], name="Staff_{}".format(number), tag=tag)
            staves.append(staff)
            self.voice_abbreviations["v{}".format(number)] = voice.name
        staff_group = abjad.StaffGroup(
            staves, name="Grouped_Staves_Staff_Group", tag=tag
        )
        score = abjad.Score([staff_group], name="Grouped_Staves_Score", tag=tag)
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
