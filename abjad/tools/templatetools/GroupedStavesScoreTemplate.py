# -*- coding: utf-8 -*-
import collections
from abjad.tools import indicatortools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class GroupedStavesScoreTemplate(AbjadObject):
    r'''Grouped staves score template.

    ::

        >>> template_class = templatetools.GroupedStavesScoreTemplate
        >>> template = template_class(staff_count=4)

    '''

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        self.context_name_abbreviations = collections.OrderedDict()
        self.staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        '''Calls score template.

        ::

            >>> score = template()

        ::

            >>> print(format(score))
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
        staves = []
        for index in range(self.staff_count):
            number = index + 1
            voice = scoretools.Voice(name='Voice {}'.format(number))
            staff = scoretools.Staff([voice], name='Staff {}'.format(number))
            staves.append(staff)
            self.context_name_abbreviations['v{}'.format(number)] = voice.name
        grouped_rhythmic_staves_staff_group = scoretools.StaffGroup(
            staves,
            name='Grouped Staves Staff Group',
            )
        grouped_rhythmic_staves_score = scoretools.Score(
            [grouped_rhythmic_staves_staff_group],
            name='Grouped Staves Score',
            )
        return grouped_rhythmic_staves_score
