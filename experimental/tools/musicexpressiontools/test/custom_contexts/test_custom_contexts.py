# -*- encoding: utf-8 -*-
from experimental import *
from abjad.tools.abctools.AbjadObject import AbjadObject


def test_custom_contexts_01():

    class CustomContextScoreTemplate(AbjadObject):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            custom_voice = scoretools.Voice(
                context_name='CustomVoice', 
                name='Custom Voice',
                )
            custom_staff = scoretools.Staff(
                context_name='CustomStaff', 
                name='Custom Staff',
                )
            custom_score = scoretools.Score(
                name='Custom Score',
                )
            custom_staff.append(custom_voice)
            custom_score.append(custom_staff)
            return custom_score

    score_template = CustomContextScoreTemplate()
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures([(4, 8), (4, 8), (4, 8)])
    score_specification.set_rhythm(library.joined_sixteenths, contexts=['Custom Voice'])
    score = score_specification.interpret()
    lilypond_file = lilypondfiletools.make_floating_time_signature_lilypond_file(score)

    context_block = lilypondfiletools.ContextBlock(
        source_context_name='Voice',
        type_='Engraver_group',
        name='CustomVoice',
        alias='Voice',
        )
    lilypond_file.layout_block.items.append(context_block)
    override(context_block).beam.color = 'green'
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

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(lilypond_file, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
