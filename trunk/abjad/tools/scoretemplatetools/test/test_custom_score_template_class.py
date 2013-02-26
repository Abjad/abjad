from abjad import *
from abjad.tools.scoretemplatetools.ScoreTemplate import ScoreTemplate


def test_custom_score_template_class_01():
    '''Score template with named contexts.
    '''

    class NamedContextScoreTemplate(ScoreTemplate):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            voice = voicetools.Voice(name='Blue Voice')
            staff = stafftools.Staff(name='Red Staff')
            score = scoretools.Score(name='Green Score')
            staff.append(voice)
            score.append(staff)
            return score

    named_context_score_template = NamedContextScoreTemplate()
    score = named_context_score_template()

    r'''
    \context Score = "Green Score" <<
        \context Staff = "Red Staff" {
            \context Voice = "Blue Voice" {
            }
        }
    >>
    '''

    assert score.lilypond_format == '\\context Score = "Green Score" <<\n\t\\context Staff = "Red Staff" {\n\t\t\\context Voice = "Blue Voice" {\n\t\t}\n\t}\n>>'


def test_custom_score_template_class_02():
    '''Score template with custom (voice and staff) contexts.

    CAUTION: always use built-in LilyPond score context; do not rename.
    '''

    class CustomContextScoreTemplate(ScoreTemplate):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            custom_voice = voicetools.Voice(context_name='CustomVoice')
            custom_staff = stafftools.Staff(context_name='CustomStaff')
            score = scoretools.Score()
            custom_staff.append(custom_voice)
            score.append(custom_staff)
            return score

    custom_context_score_template = CustomContextScoreTemplate()
    score = custom_context_score_template()

    r''' 
    \new Score <<
        \new CustomStaff {
            \new CustomVoice {
            }
        }
    >>
    '''

    assert score.lilypond_format == '\\new Score <<\n\t\\new CustomStaff {\n\t\t\\new CustomVoice {\n\t\t}\n\t}\n>>'

    # here's how to properly override with externalized layout

    score = custom_context_score_template()
    score[0][0].append("c'4 ( d'4 e'4 f'4 )")
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Voice'
    context_block.type = 'Engraver_group'
    context_block.name = 'CustomVoice'
    context_block.alias = 'Voice'
    context_block.override.note_head.color = 'green'
    context_block.override.stem.color = 'green'

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Staff'
    context_block.type = 'Engraver_group'
    context_block.name = 'CustomStaff'
    context_block.alias = 'Staff'
    context_block.accepts.append('CustomVoice')
    context_block.override.staff_symbol.color = 'red'

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Score'
    context_block.accepts.append('CustomStaff')

    r'''
    \layout {
        \context {
            \Voice
            \name CustomVoice
            \type Engraver_group
            \alias Voice
            \override NoteHead #'color = #green
            \override Stem #'color = #green
        }
        \context {
            \Staff
            \name CustomStaff
            \type Engraver_group
            \alias Staff
            \accepts CustomVoice
            \override StaffSymbol #'color = #red
        }
        \context {
            \Score
            \accepts CustomStaff
        }
    }
    '''

    assert lilypond_file.layout_block.lilypond_format == "\\layout {\n\t\\context {\n\t\t\\Voice\n\t\t\\name CustomVoice\n\t\t\\type Engraver_group\n\t\t\\alias Voice\n\t\t\\override NoteHead #'color = #green\n\t\t\\override Stem #'color = #green\n\t}\n\t\\context {\n\t\t\\Staff\n\t\t\\name CustomStaff\n\t\t\\type Engraver_group\n\t\t\\alias Staff\n\t\t\\accepts CustomVoice\n\t\t\\override StaffSymbol #'color = #red\n\t}\n\t\\context {\n\t\t\\Score\n\t\t\\accepts CustomStaff\n\t}\n}"
 
    r'''
    \score {
        \new Score <<
            \new CustomStaff {
                \new CustomVoice {
                    c'4 (
                    d'4
                    e'4
                    f'4 )
                }
            }
        >>
    }
    '''

    assert lilypond_file.score_block.lilypond_format == "\\score {\n\t\\new Score <<\n\t\t\\new CustomStaff {\n\t\t\t\\new CustomVoice {\n\t\t\t\tc'4 (\n\t\t\t\td'4\n\t\t\t\te'4\n\t\t\t\tf'4 )\n\t\t\t}\n\t\t}\n\t>>\n}"
