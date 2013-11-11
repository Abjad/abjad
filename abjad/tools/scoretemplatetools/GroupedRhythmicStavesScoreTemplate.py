# -*- encoding: utf-8 -*-
import collections
from abjad.tools import marktools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools import scoretools
from abjad.tools.abctools.AbjadObject import AbjadObject


class GroupedRhythmicStavesScoreTemplate(AbjadObject):
    r'''Grouped rhythmic staves score template.
    
    ::

            >>> from abjad.tools.scoretemplatetools import *
            >>> template_class = GroupedRhythmicStavesScoreTemplate

    ..  container:: example

        **Example 1.** One voice per staff:

        ::

            >>> template_1 = template_class(staff_count=4)

    ..  container:: example
    
        **Example 2.** More than one voice per staff:

        ::

            >>> template_2 = template_class(staff_count=[2, 1, 2])

    '''

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        assert isinstance(staff_count, (int, list))
        self.context_name_abbreviations = collections.OrderedDict()
        self._staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        r'''Calls score template.

        ..  container:: example

            **Example 1.** Call first template:

            ::

                >>> score_1 = template_1()

            ::

                >>> print format(score_1)
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

            **Example 2.** Call second template:

            ::

                >>> score_2 = template_2()

            ::

                >>> print format(score_2)
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
        staves = []
        if isinstance(self.staff_count, int):
            for index in range(self.staff_count):
                number = index + 1
                voice = scoretools.Voice(name='Voice {}'.format(number))
                staff = scoretools.RhythmicStaff(
                    [voice], name='Staff {}'.format(number))
                staves.append(staff)
                self.context_name_abbreviations['v{}'.format(number)] = \
                    voice.name
        elif isinstance(self.staff_count, list):
            for staff_index, voice_count in enumerate(self.staff_count):
                staff_number = staff_index + 1
                staff = scoretools.RhythmicStaff(
                    [], name='Staff {}'.format(staff_number))
                assert 1 <= voice_count
                for voice_index in range(voice_count):
                    voice_number = voice_index + 1
                    if voice_count == 1:
                        voice_identifier = str(staff_number)
                    else:
                        voice_identifier = '{}-{}'.format(
                            staff_number, voice_number)
                        staff.is_simultaneous = True
                    voice = scoretools.Voice(
                        name='Voice {}'.format(voice_identifier))
                    staff.append(voice)
                    self.context_name_abbreviations[
                        'v{}'.format(voice_identifier)] = voice.name
                staves.append(staff)
        grouped_rhythmic_staves_staff_group = scoretools.StaffGroup(
            staves, 
            name='Grouped Rhythmic Staves Staff Group',
            )
        grouped_rhythmic_staves_score = scoretools.Score(
            [grouped_rhythmic_staves_staff_group], 
            name='Grouped Rhythmic Staves Score',
            )
        return grouped_rhythmic_staves_score

    ### PUBLIC PROPERTIES ###

    @property
    def staff_count(self):
        r'''Score template staff count.

        ::

            >>> template_1.staff_count
            4

        Returns nonnegative integer.
        '''
        return self._staff_count
