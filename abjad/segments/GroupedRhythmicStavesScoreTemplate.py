import collections
from abjad.utilities.OrderedDict import OrderedDict
from .ScoreTemplate import ScoreTemplate


class GroupedRhythmicStavesScoreTemplate(ScoreTemplate):
    r"""
    Grouped rhythmic staves score template.

    ..  container:: example

        One voice per staff:

        >>> class_ = abjad.GroupedRhythmicStavesScoreTemplate
        >>> template_1 = class_(staff_count=4)
        >>> abjad.show(template_1) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(template_1.__illustrate__()[abjad.Score], strict=60)
            \context Score = "Grouped_Rhythmic_Staves_Score"            %! GroupedRhythmicStavesScoreTemplate
            <<                                                          %! GroupedRhythmicStavesScoreTemplate
                \context StaffGroup = "Grouped_Rhythmic_Staves_Staff_Group" %! GroupedRhythmicStavesScoreTemplate
                <<                                                      %! GroupedRhythmicStavesScoreTemplate
                    \context RhythmicStaff = "Staff_1"                  %! GroupedRhythmicStavesScoreTemplate
                    {                                                   %! GroupedRhythmicStavesScoreTemplate
                        \context Voice = "Voice_1"                      %! GroupedRhythmicStavesScoreTemplate
                        {                                               %! GroupedRhythmicStavesScoreTemplate
                            \clef "percussion"                          %! attach_defaults
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                                   %! GroupedRhythmicStavesScoreTemplate
                    \context RhythmicStaff = "Staff_2"                  %! GroupedRhythmicStavesScoreTemplate
                    {                                                   %! GroupedRhythmicStavesScoreTemplate
                        \context Voice = "Voice_2"                      %! GroupedRhythmicStavesScoreTemplate
                        {                                               %! GroupedRhythmicStavesScoreTemplate
                            \clef "percussion"                          %! attach_defaults
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                                   %! GroupedRhythmicStavesScoreTemplate
                    \context RhythmicStaff = "Staff_3"                  %! GroupedRhythmicStavesScoreTemplate
                    {                                                   %! GroupedRhythmicStavesScoreTemplate
                        \context Voice = "Voice_3"                      %! GroupedRhythmicStavesScoreTemplate
                        {                                               %! GroupedRhythmicStavesScoreTemplate
                            \clef "percussion"                          %! attach_defaults
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                                   %! GroupedRhythmicStavesScoreTemplate
                    \context RhythmicStaff = "Staff_4"                  %! GroupedRhythmicStavesScoreTemplate
                    {                                                   %! GroupedRhythmicStavesScoreTemplate
                        \context Voice = "Voice_4"                      %! GroupedRhythmicStavesScoreTemplate
                        {                                               %! GroupedRhythmicStavesScoreTemplate
                            \clef "percussion"                          %! attach_defaults
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                                   %! GroupedRhythmicStavesScoreTemplate
                >>                                                      %! GroupedRhythmicStavesScoreTemplate
            >>                                                          %! GroupedRhythmicStavesScoreTemplate

        >>> score = template_1()
        >>> abjad.show(score) # doctest: +SKIP

        >>> abjad.f(score, strict=60)
        \context Score = "Grouped_Rhythmic_Staves_Score"            %! GroupedRhythmicStavesScoreTemplate
        <<                                                          %! GroupedRhythmicStavesScoreTemplate
            \context StaffGroup = "Grouped_Rhythmic_Staves_Staff_Group" %! GroupedRhythmicStavesScoreTemplate
            <<                                                      %! GroupedRhythmicStavesScoreTemplate
                \context RhythmicStaff = "Staff_1"                  %! GroupedRhythmicStavesScoreTemplate
                {                                                   %! GroupedRhythmicStavesScoreTemplate
                    \context Voice = "Voice_1"                      %! GroupedRhythmicStavesScoreTemplate
                    {                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                               %! GroupedRhythmicStavesScoreTemplate
                }                                                   %! GroupedRhythmicStavesScoreTemplate
                \context RhythmicStaff = "Staff_2"                  %! GroupedRhythmicStavesScoreTemplate
                {                                                   %! GroupedRhythmicStavesScoreTemplate
                    \context Voice = "Voice_2"                      %! GroupedRhythmicStavesScoreTemplate
                    {                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                               %! GroupedRhythmicStavesScoreTemplate
                }                                                   %! GroupedRhythmicStavesScoreTemplate
                \context RhythmicStaff = "Staff_3"                  %! GroupedRhythmicStavesScoreTemplate
                {                                                   %! GroupedRhythmicStavesScoreTemplate
                    \context Voice = "Voice_3"                      %! GroupedRhythmicStavesScoreTemplate
                    {                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                               %! GroupedRhythmicStavesScoreTemplate
                }                                                   %! GroupedRhythmicStavesScoreTemplate
                \context RhythmicStaff = "Staff_4"                  %! GroupedRhythmicStavesScoreTemplate
                {                                                   %! GroupedRhythmicStavesScoreTemplate
                    \context Voice = "Voice_4"                      %! GroupedRhythmicStavesScoreTemplate
                    {                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                               %! GroupedRhythmicStavesScoreTemplate
                }                                                   %! GroupedRhythmicStavesScoreTemplate
            >>                                                      %! GroupedRhythmicStavesScoreTemplate
        >>                                                          %! GroupedRhythmicStavesScoreTemplate

    ..  container:: example

        More than one voice per staff:

        >>> template_2 = class_(staff_count=[2, 1, 2])
        >>> abjad.show(template_2) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(template_2.__illustrate__()[abjad.Score], strict=60)
            \context Score = "Grouped_Rhythmic_Staves_Score"            %! GroupedRhythmicStavesScoreTemplate
            <<                                                          %! GroupedRhythmicStavesScoreTemplate
                \context StaffGroup = "Grouped_Rhythmic_Staves_Staff_Group" %! GroupedRhythmicStavesScoreTemplate
                <<                                                      %! GroupedRhythmicStavesScoreTemplate
                    \context RhythmicStaff = "Staff_1"                  %! GroupedRhythmicStavesScoreTemplate
                    <<                                                  %! GroupedRhythmicStavesScoreTemplate
                        \context Voice = "Voice_1_1"                    %! GroupedRhythmicStavesScoreTemplate
                        {                                               %! GroupedRhythmicStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedRhythmicStavesScoreTemplate
                        \context Voice = "Voice_1_2"                    %! GroupedRhythmicStavesScoreTemplate
                        {                                               %! GroupedRhythmicStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedRhythmicStavesScoreTemplate
                    >>                                                  %! GroupedRhythmicStavesScoreTemplate
                    \context RhythmicStaff = "Staff_2"                  %! GroupedRhythmicStavesScoreTemplate
                    {                                                   %! GroupedRhythmicStavesScoreTemplate
                        \context Voice = "Voice_2"                      %! GroupedRhythmicStavesScoreTemplate
                        {                                               %! GroupedRhythmicStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                                   %! GroupedRhythmicStavesScoreTemplate
                    \context RhythmicStaff = "Staff_3"                  %! GroupedRhythmicStavesScoreTemplate
                    <<                                                  %! GroupedRhythmicStavesScoreTemplate
                        \context Voice = "Voice_3_1"                    %! GroupedRhythmicStavesScoreTemplate
                        {                                               %! GroupedRhythmicStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedRhythmicStavesScoreTemplate
                        \context Voice = "Voice_3_2"                    %! GroupedRhythmicStavesScoreTemplate
                        {                                               %! GroupedRhythmicStavesScoreTemplate
                            s1                                          %! ScoreTemplate.__illustrate__
                        }                                               %! GroupedRhythmicStavesScoreTemplate
                    >>                                                  %! GroupedRhythmicStavesScoreTemplate
                >>                                                      %! GroupedRhythmicStavesScoreTemplate
            >>                                                          %! GroupedRhythmicStavesScoreTemplate

        >>> score = template_2()
        >>> abjad.show(score) # doctest: +SKIP

        >>> abjad.f(score, strict=60)
        \context Score = "Grouped_Rhythmic_Staves_Score"            %! GroupedRhythmicStavesScoreTemplate
        <<                                                          %! GroupedRhythmicStavesScoreTemplate
            \context StaffGroup = "Grouped_Rhythmic_Staves_Staff_Group" %! GroupedRhythmicStavesScoreTemplate
            <<                                                      %! GroupedRhythmicStavesScoreTemplate
                \context RhythmicStaff = "Staff_1"                  %! GroupedRhythmicStavesScoreTemplate
                <<                                                  %! GroupedRhythmicStavesScoreTemplate
                    \context Voice = "Voice_1_1"                    %! GroupedRhythmicStavesScoreTemplate
                    {                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                               %! GroupedRhythmicStavesScoreTemplate
                    \context Voice = "Voice_1_2"                    %! GroupedRhythmicStavesScoreTemplate
                    {                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                               %! GroupedRhythmicStavesScoreTemplate
                >>                                                  %! GroupedRhythmicStavesScoreTemplate
                \context RhythmicStaff = "Staff_2"                  %! GroupedRhythmicStavesScoreTemplate
                {                                                   %! GroupedRhythmicStavesScoreTemplate
                    \context Voice = "Voice_2"                      %! GroupedRhythmicStavesScoreTemplate
                    {                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                               %! GroupedRhythmicStavesScoreTemplate
                }                                                   %! GroupedRhythmicStavesScoreTemplate
                \context RhythmicStaff = "Staff_3"                  %! GroupedRhythmicStavesScoreTemplate
                <<                                                  %! GroupedRhythmicStavesScoreTemplate
                    \context Voice = "Voice_3_1"                    %! GroupedRhythmicStavesScoreTemplate
                    {                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                               %! GroupedRhythmicStavesScoreTemplate
                    \context Voice = "Voice_3_2"                    %! GroupedRhythmicStavesScoreTemplate
                    {                                               %! GroupedRhythmicStavesScoreTemplate
                    }                                               %! GroupedRhythmicStavesScoreTemplate
                >>                                                  %! GroupedRhythmicStavesScoreTemplate
            >>                                                      %! GroupedRhythmicStavesScoreTemplate
        >>                                                          %! GroupedRhythmicStavesScoreTemplate

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_staff_count',
        )

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        super().__init__()
        assert isinstance(staff_count, (int, collections.Iterable))
        if isinstance(staff_count, collections.Iterable):
            staff_count = list(staff_count)
        self._staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls score template.

        Returns score.
        """
        import abjad
        staves = []
        tag = 'GroupedRhythmicStavesScoreTemplate'
        if isinstance(self.staff_count, int):
            for index in range(self.staff_count):
                number = index + 1
                name = 'Voice_{}'.format(number)
                voice = abjad.Voice([], name=name, tag=tag)
                name = 'Staff_{}'.format(number)
                staff = abjad.Staff([voice], name=name, tag=tag)
                staff.lilypond_type = 'RhythmicStaff'
                abjad.annotate(staff, 'default_clef', abjad.Clef('percussion'))
                staves.append(staff)
                key = 'v{}'.format(number)
                self.voice_abbreviations[key] = voice.name
        elif isinstance(self.staff_count, list):
            for staff_index, voice_count in enumerate(self.staff_count):
                staff_number = staff_index + 1
                name = 'Staff_{}'.format(staff_number)
                staff = abjad.Staff(name=name, tag=tag)
                staff.lilypond_type = 'RhythmicStaff'
                assert 1 <= voice_count
                for voice_index in range(voice_count):
                    voice_number = voice_index + 1
                    if voice_count == 1:
                        voice_identifier = str(staff_number)
                    else:
                        voice_identifier = '{}_{}'.format(
                            staff_number, voice_number)
                        staff.is_simultaneous = True
                    name = 'Voice_{}'.format(voice_identifier)
                    voice = abjad.Voice([], name=name, tag=tag)
                    staff.append(voice)
                    key = 'v{}'.format(voice_identifier)
                    self.voice_abbreviations[key] = voice.name
                staves.append(staff)
        grouped_rhythmic_staves_staff_group = abjad.StaffGroup(
            staves,
            name='Grouped_Rhythmic_Staves_Staff_Group',
            tag=tag,
            )
        grouped_rhythmic_staves_score = abjad.Score(
            [grouped_rhythmic_staves_staff_group],
            name='Grouped_Rhythmic_Staves_Score',
            tag=tag,
            )
        return grouped_rhythmic_staves_score

    ### PUBLIC PROPERTIES ###

    @property
    def staff_count(self):
        """
        Gets score template staff count.

        ..  container:: example

            >>> class_ = abjad.GroupedRhythmicStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.staff_count
            4

        Returns nonnegative integer.
        """
        return self._staff_count

    @property
    def voice_abbreviations(self):
        """
        Gets context name abbreviations.

        ..  container:: example

            >>> class_ = abjad.GroupedRhythmicStavesScoreTemplate
            >>> template = class_(staff_count=4)
            >>> template.voice_abbreviations
            OrderedDict([])

        """
        return super(
            GroupedRhythmicStavesScoreTemplate,
            self,
            ).voice_abbreviations
