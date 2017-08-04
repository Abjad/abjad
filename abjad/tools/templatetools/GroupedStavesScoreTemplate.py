# -*- coding: utf-8 -*-
import collections
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class GroupedStavesScoreTemplate(AbjadValueObject):
    r'''Grouped staves score template.

    ::

        >>> import abjad

    ..  container:: example

        ::

            >>> template_class = abjad.templatetools.GroupedStavesScoreTemplate
            >>> template = template_class(staff_count=4)

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context_name_abbreviations',
        '_staff_count',
        )

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        self._context_name_abbreviations = collections.OrderedDict()
        self._staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Calls score template.

        ..  container:: example

            ::

                >>> score = template()
                >>> show(score) # doctest: +SKIP

            ::

                >>> f(score)
                \context Score = "Grouped Staves Score" <<
                    \context StaffGroup = "Grouped Staves Staff Group" <<
                        \context Staff = "Staff 1" {
                            \context Voice = "Voice 1" {
                            }
                        }
                        \context Staff = "Staff 2" {
                            \context Voice = "Voice 2" {
                            }
                        }
                        \context Staff = "Staff 3" {
                            \context Voice = "Voice 3" {
                            }
                        }
                        \context Staff = "Staff 4" {
                            \context Voice = "Voice 4" {
                            }
                        }
                    >>
                >>

        Returns score.
        '''
        import abjad
        staves = []
        for index in range(self.staff_count):
            number = index + 1
            voice = abjad.Voice(
                [],
                name='Voice {}'.format(number),
                )
            staff = abjad.Staff(
                [voice],
                name='Staff {}'.format(number),
                )
            staves.append(staff)
            self.context_name_abbreviations['v{}'.format(number)] = voice.name
        grouped_rhythmic_staves_staff_group = abjad.StaffGroup(
            staves,
            name='Grouped Staves Staff Group',
            )
        grouped_rhythmic_staves_score = abjad.Score(
            [grouped_rhythmic_staves_staff_group],
            name='Grouped Staves Score',
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
        r'''Gets staff count.
        '''
        return self._staff_count
