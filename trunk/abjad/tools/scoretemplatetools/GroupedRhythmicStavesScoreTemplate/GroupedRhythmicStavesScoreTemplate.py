import collections
from abjad.tools import contexttools
from abjad.tools import instrumenttools
from abjad.tools import scoretools
from abjad.tools import stafftools
from abjad.tools import voicetools
from abjad.tools.scoretemplatetools.ScoreTemplate import ScoreTemplate


class GroupedRhythmicStavesScoreTemplate(ScoreTemplate):
    r'''.. versionadded:: 2.9

    Example 1. Grouped rhythmic staves score template with one voice per staff::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=4)
        >>> score = template()

    ::

        >>> score
        Score-"Grouped Rhythmic Staves Score"<<1>>

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

    Example 2. Grouped rhythmic staves score template with more than one voice per staff::

        >>> template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=[2, 1, 2])
        >>> score = template()

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

    Return score template object.   
    '''

    ### INITIALIZER ###

    def __init__(self, staff_count=2):
        assert isinstance(staff_count, (int, list))
        self.context_name_abbreviations = collections.OrderedDict()
        self._staff_count = staff_count

    ### SPECIAL METHODS ###

    def __call__(self):
        staves = []
        if isinstance(self.staff_count, int):
            for index in range(self.staff_count):
                number = index + 1
                voice = voicetools.Voice(name='Voice {}'.format(number))     
                staff = stafftools.RhythmicStaff([voice], name='Staff {}'.format(number))
                staves.append(staff)
                self.context_name_abbreviations['v{}'.format(number)] = voice.name
        elif isinstance(self.staff_count, list):
            for staff_index, voice_count in enumerate(self.staff_count):
                staff_number = staff_index + 1
                staff = stafftools.RhythmicStaff([], name='Staff {}'.format(staff_number))
                assert 1 <= voice_count  
                for voice_index in range(voice_count):
                    voice_number = voice_index + 1
                    if voice_count == 1:
                        voice_identifier = str(staff_number)
                    else:
                        voice_identifier = '{}-{}'.format(staff_number, voice_number)
                        staff.is_parallel = True
                    voice = voicetools.Voice(name='Voice {}'.format(voice_identifier))
                    staff.append(voice)
                    self.context_name_abbreviations['v{}'.format(voice_identifier)] = voice.name
                staves.append(staff)
        
        grouped_rhythmic_staves_staff_group = scoretools.StaffGroup(
            staves, name='Grouped Rhythmic Staves Staff Group')         

        grouped_rhythmic_staves_score = scoretools.Score(
            [grouped_rhythmic_staves_staff_group], name='Grouped Rhythmic Staves Score')

        return grouped_rhythmic_staves_score

    ### READ-ONLY PUBLIC PROPERTIES ###

    @property
    def staff_count(self):
        return self._staff_count
