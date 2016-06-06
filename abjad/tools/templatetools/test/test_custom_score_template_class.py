# -*- coding: utf-8 -*-
from abjad import *
from abjad.tools.abctools.AbjadObject import AbjadObject


def test_custom_score_template_class_01():
    r'''Score template with named contexts.
    '''

    class NamedContextScoreTemplate(AbjadObject):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            voice = scoretools.Voice(name='Blue Voice')
            staff = scoretools.Staff(name='Red Staff')
            score = scoretools.Score(name='Green Score')
            staff.append(voice)
            score.append(staff)
            return score

    named_context_score_template = NamedContextScoreTemplate()
    score = named_context_score_template()

    assert format(score) == stringtools.normalize(
        r'''
        \context Score = "Green Score" <<
            \context Staff = "Red Staff" {
                \context Voice = "Blue Voice" {
                }
            }
        >>
        '''
        )


def test_custom_score_template_class_02():
    r'''Score template with custom (voice and staff) contexts.

    CAUTION: always use built-in LilyPond score context; do not rename.
    '''

    class CustomContextScoreTemplate(AbjadObject):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            custom_voice = scoretools.Voice(context_name='CustomVoice')
            custom_staff = scoretools.Staff(context_name='CustomStaff')
            score = scoretools.Score()
            custom_staff.append(custom_voice)
            score.append(custom_staff)
            return score

    custom_context_score_template = CustomContextScoreTemplate()
    score = custom_context_score_template()

    assert format(score) == stringtools.normalize(
        r'''
        \new Score <<
            \new CustomStaff {
                \new CustomVoice {
                }
            }
        >>
        '''
        )

    # here's how to properly override with externalized layout

    score = custom_context_score_template()
    score[0][0].append("c'4 ( d'4 e'4 f'4 )")
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Voice',
        type_='Engraver_group',
        name='CustomVoice',
        alias='Voice',
        )
    lilypond_file.layout_block.items.append(context_block)
    override(context_block).note_head.color = 'green'
    override(context_block).stem.color = 'green'

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Staff',
        type_='Engraver_group',
        name='CustomStaff',
        alias='Staff',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.accepts_commands.append('CustomVoice')
    override(context_block).staff_symbol.color = 'red'

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Score',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.accepts_commands.append('CustomStaff')

    assert format(lilypond_file.layout_block) == stringtools.normalize(
        r'''
        \layout {
            \context {
                \Voice
                \name CustomVoice
                \type Engraver_group
                \alias Voice
                \override NoteHead.color = #green
                \override Stem.color = #green
            }
            \context {
                \Staff
                \name CustomStaff
                \type Engraver_group
                \alias Staff
                \accepts CustomVoice
                \override StaffSymbol.color = #red
            }
            \context {
                \Score
                \accepts CustomStaff
            }
        }
        '''
        )

    assert format(lilypond_file.score_block) == stringtools.normalize(
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
        )
