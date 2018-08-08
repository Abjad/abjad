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
            \context Score = "Grouped Staves Score"                     %! GroupedStavesScoreTemplate
            <<                                                          %! GroupedStavesScoreTemplate
                \context StaffGroup = "Grouped Staves Staff Group"      %! GroupedStavesScoreTemplate
                <<                                                      %! GroupedStavesScoreTemplate
                    \context Staff = "Staff 1"                          %! GroupedStavesScoreTemplate
                    {                                                   %! GroupedStavesScoreTemplate
                        \context Voice = "Voice 1"                      %! GroupedStavesScoreTemplate
                        {                                               %! GroupedStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedStavesScoreTemplate
                    }                                                   %! GroupedStavesScoreTemplate
                    \context Staff = "Staff 2"                          %! GroupedStavesScoreTemplate
                    {                                                   %! GroupedStavesScoreTemplate
                        \context Voice = "Voice 2"                      %! GroupedStavesScoreTemplate
                        {                                               %! GroupedStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedStavesScoreTemplate
                    }                                                   %! GroupedStavesScoreTemplate
                    \context Staff = "Staff 3"                          %! GroupedStavesScoreTemplate
                    {                                                   %! GroupedStavesScoreTemplate
                        \context Voice = "Voice 3"                      %! GroupedStavesScoreTemplate
                        {                                               %! GroupedStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedStavesScoreTemplate
                    }                                                   %! GroupedStavesScoreTemplate
                    \context Staff = "Staff 4"                          %! GroupedStavesScoreTemplate
                    {                                                   %! GroupedStavesScoreTemplate
                        \context Voice = "Voice 4"                      %! GroupedStavesScoreTemplate
                        {                                               %! GroupedStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedStavesScoreTemplate
                    }                                                   %! GroupedStavesScoreTemplate
                >>                                                      %! GroupedStavesScoreTemplate
            >>                                                          %! GroupedStavesScoreTemplate

        >>> score = template()
        >>> abjad.f(score, strict=60)
        \context Score = "Grouped Staves Score"                     %! GroupedStavesScoreTemplate
        <<                                                          %! GroupedStavesScoreTemplate
            \context StaffGroup = "Grouped Staves Staff Group"      %! GroupedStavesScoreTemplate
            <<                                                      %! GroupedStavesScoreTemplate
                \context Staff = "Staff 1"                          %! GroupedStavesScoreTemplate
                {                                                   %! GroupedStavesScoreTemplate
                    \context Voice = "Voice 1"                      %! GroupedStavesScoreTemplate
                    {                                               %! GroupedStavesScoreTemplate
                    }                                               %! GroupedStavesScoreTemplate
                }                                                   %! GroupedStavesScoreTemplate
                \context Staff = "Staff 2"                          %! GroupedStavesScoreTemplate
                {                                                   %! GroupedStavesScoreTemplate
                    \context Voice = "Voice 2"                      %! GroupedStavesScoreTemplate
                    {                                               %! GroupedStavesScoreTemplate
                    }                                               %! GroupedStavesScoreTemplate
                }                                                   %! GroupedStavesScoreTemplate
                \context Staff = "Staff 3"                          %! GroupedStavesScoreTemplate
                {                                                   %! GroupedStavesScoreTemplate
                    \context Voice = "Voice 3"                      %! GroupedStavesScoreTemplate
                    {                                               %! GroupedStavesScoreTemplate
                    }                                               %! GroupedStavesScoreTemplate
                }                                                   %! GroupedStavesScoreTemplate
                \context Staff = "Staff 4"                          %! GroupedStavesScoreTemplate
                {                                                   %! GroupedStavesScoreTemplate
                    \context Voice = "Voice 4"                      %! GroupedStavesScoreTemplate
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
                name='Voice {}'.format(number),
                tag=tag,
                )
            staff = abjad.Staff(
                [voice],
                name='Staff {}'.format(number),
                tag=tag,
                )
            staves.append(staff)
            self.voice_abbreviations['v{}'.format(number)] = voice.name
        staff_group = abjad.StaffGroup(
            staves,
            name='Grouped Staves Staff Group',
            tag=tag,
            )
        score = abjad.Score(
            [staff_group],
            name='Grouped Staves Score',
            tag=tag,
            )
        return score

    ### PUBLIC PROPERTIES ###

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
