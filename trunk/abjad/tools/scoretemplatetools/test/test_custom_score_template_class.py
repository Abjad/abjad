from abjad import *
from abjad.tools.scoretemplatetools.ScoreTemplate import ScoreTemplate


def test_custom_score_template_class_01():

    class FooScoreTemplate(ScoreTemplate):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            custom_voice = voicetools.Voice(name='Custom Voice')
            custom_staff = stafftools.Staff(name='Custom Staff')
            custom_score = scoretools.Score(name='Custom Score')
            custom_staff.append(custom_voice)
            custom_score.append(custom_staff)
            return custom_score

    foo_score_template = FooScoreTemplate()
    foo_score = foo_score_template()

    r'''
    \context Score = "Custom Score" <<
        \context Staff = "Custom Staff" {
            \context Voice = "Custom Voice" {
            }
        }
    >>
    '''

    assert foo_score.lilypond_format == '\\context Score = "Custom Score" <<\n\t\\context Staff = "Custom Staff" {\n\t\t\\context Voice = "Custom Voice" {\n\t\t}\n\t}\n>>'


def test_custom_score_template_class_02():

    class CustomContextScoreTemplate(ScoreTemplate):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            custom_voice = voicetools.Voice(context_name='CustomVoice', name='Custom Voice')
            custom_staff = stafftools.Staff(context_name='CustomStaff', name='Custom Staff')
            custom_score = scoretools.Score(context_name='CustomScore', name='Custom Score')
            custom_staff.append(custom_voice)
            custom_score.append(custom_staff)
            return custom_score

    custom_context_score_template = CustomContextScoreTemplate()
    custom_context_score = custom_context_score_template()

    r''' 
    \context CustomScore = "Custom Score" <<
        \context CustomStaff = "Custom Staff" {
            \context CustomVoice = "Custom Voice" {
            }
        }
    >>
    '''

    assert custom_context_score.lilypond_format == '\\context CustomScore = "Custom Score" <<\n\t\\context CustomStaff = "Custom Staff" {\n\t\t\\context CustomVoice = "Custom Voice" {\n\t\t}\n\t}\n>>'
