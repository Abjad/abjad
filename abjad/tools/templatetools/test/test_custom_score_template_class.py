# -*- coding: utf-8 -*-
import abjad


# TODO: Move to doctests
def test_custom_score_template_class_01():
    r'''Score template with named contexts.
    '''

    class NamedContextScoreTemplate(abjad.abctools.AbjadObject):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            voice = abjad.Voice(name='Blue Voice')
            staff = abjad.Staff(name='Red Staff')
            score = abjad.Score(name='Green Score')
            staff.append(voice)
            score.append(staff)
            return score

    named_context_score_template = NamedContextScoreTemplate()
    score = named_context_score_template()

    assert format(score) == abjad.String.normalize(
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

    class CustomContextScoreTemplate(abjad.abctools.AbjadObject):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            custom_voice = abjad.Voice(context_name='CustomVoice')
            custom_staff = abjad.Staff(context_name='CustomStaff')
            score = abjad.Score()
            custom_staff.append(custom_voice)
            score.append(custom_staff)
            return score

    custom_context_score_template = CustomContextScoreTemplate()
    score = custom_context_score_template()

    assert format(score) == abjad.String.normalize(
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
    lilypond_file = abjad.LilyPondFile.new(score)

    context_block = abjad.ContextBlock(
        source_context_name='Voice',
        type_='Engraver_group',
        name='CustomVoice',
        alias='Voice',
        )
    lilypond_file.layout_block.items.append(context_block)
    abjad.override(context_block).note_head.color = 'green'
    abjad.override(context_block).stem.color = 'green'

    context_block = abjad.ContextBlock(
        source_context_name='Staff',
        type_='Engraver_group',
        name='CustomStaff',
        alias='Staff',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.accepts_commands.append('CustomVoice')
    abjad.override(context_block).staff_symbol.color = 'red'

    context_block = abjad.ContextBlock(
        source_context_name='Score',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.accepts_commands.append('CustomStaff')

    assert format(lilypond_file.layout_block) == abjad.String.normalize(
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

    assert format(lilypond_file.score_block) == abjad.String.normalize(
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
