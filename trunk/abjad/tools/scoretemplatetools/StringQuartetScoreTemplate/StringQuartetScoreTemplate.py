from abjad.tools import contexttools
from abjad.tools import scoretools
from abjad.tools import stafftools
from abjad.tools import voicetools
from abjad.tools.scoretemplatetools.ScoreTemplate import ScoreTemplate


class StringQuartetScoreTemplate(ScoreTemplate):
    '''.. versionadded:: 2.8

    String quartet score template::

        abjad> from abjad.tools import scoretemplatetools

    ::

        abjad> template = scoretemplatetools.StringQuartetScoreTemplate()
        abjad> score = template()

    ::

        abjad> score
        Score-"String Quartet Score"<<1>>

    ::

        abjad> f(score)
        \context Score = "String Quartet Score" <<
            \context StaffGroup = "String Quartet Staff Group" <<
                \context Staff = "First Violin Staff" {
                    \clef "treble"
                    \context Voice = "First Violin Voice" {
                    }
                }
                \context Staff = "Second Violin Voice" {
                    \clef "treble"
                }
                \context Staff = "Viola Staff" {
                    \clef "alto"
                }
                \context Staff = "Cello Staff" {
                    \clef "bass"
                }
            >>
        >>

    Return score template.
    '''

    ### INITIALIZER ###

    def __init__(self):
        pass

    ### SPECIAL METHODS ###

    def __call__(self):

        # make first violin voice and staff
        first_violin_voice = voicetools.Voice(name='First Violin Voice')
        first_violin_staff = stafftools.Staff([first_violin_voice], name='First Violin Staff')
        contexttools.ClefMark('treble')(first_violin_staff)

        # make second violin voice and staff
        second_violin_voice = voicetools.Voice(name='Second Violin Voice')
        second_violin_staff = stafftools.Staff(name='Second Violin Voice')
        contexttools.ClefMark('treble')(second_violin_staff)

        # make viola voice and staff
        viola_voice = voicetools.Voice(name='Viola Voice')
        viola_staff = stafftools.Staff(name='Viola Staff')
        contexttools.ClefMark('alto')(viola_staff)

        # make cello voice and staff
        cello_voice = voicetools.Voice(name='Cello Voice')
        cello_staff = stafftools.Staff(name='Cello Staff')
        contexttools.ClefMark('bass')(cello_staff)

        # make string quartet staff group
        string_quartet_staff_group = scoretools.StaffGroup([
            first_violin_staff,
            second_violin_staff,
            viola_staff,
            cello_staff,
            ],
            name='String Quartet Staff Group',
            )

        # make string quartet score
        string_quartet_score = scoretools.Score(
            [string_quartet_staff_group],
            name='String Quartet Score',
            )

        # return string quartet score
        return string_quartet_score
