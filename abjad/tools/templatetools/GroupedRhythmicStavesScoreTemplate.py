# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class GroupedRhythmicStavesScoreTemplate(AbjadValueObject):
    r'''Grouped rhythmic staves score template.

    ::

        >>> import abjad

    ..  container:: example

        One voice per staff:

        ::

            >>> class_ = abjad.templatetools.GroupedRhythmicStavesScoreTemplate
            >>> template_1 = class_(staff_count=4)
            >>> score = template_1()
            >>> show(score) # doctest: +SKIP

        ::

            >>> f(score)
            \context Score = "Grouped Rhythmic Staves Score" <<
                \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
                    \context RhythmicStaff = "Staff 1" {
                        \context Voice = "Voice 1" {
                        }
                    }
                    \context RhythmicStaff = "Staff 2" {
                        \context Voice = "Voice 2" {
                        }
                    }
                    \context RhythmicStaff = "Staff 3" {
                        \context Voice = "Voice 3" {
                        }
                    }
                    \context RhythmicStaff = "Staff 4" {
                        \context Voice = "Voice 4" {
                        }
                    }
                >>
            >>

    ..  container:: example

        More than one voice per staff:

        ::

            >>> template_2 = class_(staff_count=[2, 1, 2])
            >>> score = template_2()
            >>> show(score) # doctest: +SKIP

        ::

            >>> f(score)
            \context Score = "Grouped Rhythmic Staves Score" <<
                \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
                    \context RhythmicStaff = "Staff 1" <<
                        \context Voice = "Voice 1-1" {
                        }
                        \context Voice = "Voice 1-2" {
                        }
                    >>
                    \context RhythmicStaff = "Staff 2" {
                        \context Voice = "Voice 2" {
                        }
                    }
                    \context RhythmicStaff = "Staff 3" <<
                        \context Voice = "Voice 3-1" {
                        }
                        \context Voice = "Voice 3-2" {
                        }
                    >>
                >>
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_name_abbreviations',
        '_staff_count',
        )

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        self._context_name_abbreviations = collections.OrderedDict()
        assert isinstance(staff_count, (int, collections.Iterable))
        if isinstance(staff_count, collections.Iterable):
            staff_count = list(staff_count)
        self._staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls score template.

        ..  container:: example

            Call first template:

            ::

                >>> score_1 = template_1()
                >>> show(score_1) # doctest: +SKIP

            ::

                >>> f(score_1)
                \context Score = "Grouped Rhythmic Staves Score" <<
                    \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
                        \context RhythmicStaff = "Staff 1" {
                            \context Voice = "Voice 1" {
                            }
                        }
                        \context RhythmicStaff = "Staff 2" {
                            \context Voice = "Voice 2" {
                            }
                        }
                        \context RhythmicStaff = "Staff 3" {
                            \context Voice = "Voice 3" {
                            }
                        }
                        \context RhythmicStaff = "Staff 4" {
                            \context Voice = "Voice 4" {
                            }
                        }
                    >>
                >>

        ..  container:: example

            Call second template:

            ::

                >>> score_2 = template_2()
                >>> show(score_2) # doctest: +SKIP

            ::

                >>> f(score_2)
                \context Score = "Grouped Rhythmic Staves Score" <<
                    \context StaffGroup = "Grouped Rhythmic Staves Staff Group" <<
                        \context RhythmicStaff = "Staff 1" <<
                            \context Voice = "Voice 1-1" {
                            }
                            \context Voice = "Voice 1-2" {
                            }
                        >>
                        \context RhythmicStaff = "Staff 2" {
                            \context Voice = "Voice 2" {
                            }
                        }
                        \context RhythmicStaff = "Staff 3" <<
                            \context Voice = "Voice 3-1" {
                            }
                            \context Voice = "Voice 3-2" {
                            }
                        >>
                    >>
                >>

        Returns score.
        '''
        import abjad
        staves = []
        if isinstance(self.staff_count, int):
            for index in range(self.staff_count):
                number = index + 1
                name = 'Voice {}'.format(number)
                voice = abjad.Voice([], name=name)
                name='Staff {}'.format(number)
                staff = abjad.Staff([voice], name=name)
                staff.context_name = 'RhythmicStaff'
                staves.append(staff)
                key = 'v{}'.format(number)
                self.context_name_abbreviations[key] = voice.name
        elif isinstance(self.staff_count, list):
            for staff_index, voice_count in enumerate(self.staff_count):
                staff_number = staff_index + 1
                name = 'Staff {}'.format(staff_number)
                staff = abjad.Staff(name=name)
                staff.context_name = 'RhythmicStaff'
                assert 1 <= voice_count
                for voice_index in range(voice_count):
                    voice_number = voice_index + 1
                    if voice_count == 1:
                        voice_identifier = str(staff_number)
                    else:
                        voice_identifier = '{}-{}'.format(
                            staff_number, voice_number)
                        staff.is_simultaneous = True
                    name = 'Voice {}'.format(voice_identifier)
                    voice = abjad.Voice([], name=name)
                    staff.append(voice)
                    key = 'v{}'.format(voice_identifier)
                    self.context_name_abbreviations[key] = voice.name
                staves.append(staff)
        grouped_rhythmic_staves_staff_group = abjad.StaffGroup(
            staves,
            name='Grouped Rhythmic Staves Staff Group',
            )
        grouped_rhythmic_staves_score = abjad.Score(
            [grouped_rhythmic_staves_staff_group],
            name='Grouped Rhythmic Staves Score',
            )
        return grouped_rhythmic_staves_score

    ### PUBLIC PROPERTIES ###

    @property
    def context_name_abbreviations(self):
        r'''Gets context name abbreviations.
        '''
        return self._context_name_abbreviations

    @property
    def staff_count(self):
        r'''Score template staff count.

        ::

            >>> template_1.staff_count
            4

        Returns nonnegative integer.
        '''
        return self._staff_count
