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
    score_specification.set_rhythm(library.sixteenths, contexts=['Custom Voice'])
    score = score_specification.interpret()
    lilypond_file = lilypondfiletools.make_floating_time_signature_lilypond_file(score)

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Voice'
    context_block.type = 'Engraver_group'
    context_block.name = 'CustomVoice'
    context_block.alias = 'Voice'
    override(context_block).beam.color = 'green'
    override(context_block).note_head.color = 'green'
    override(context_block).stem.color = 'green'

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Staff'
    context_block.type = 'Engraver_group'
    context_block.name = 'CustomStaff'
    context_block.alias = 'Staff'
    context_block.accepts.append('CustomVoice')
    override(context_block).staff_symbol.color = 'red'

    context_block = lilypondfiletools.ContextBlock()
    lilypond_file.layout_block.context_blocks.append(context_block)
    context_block.context_name = 'Score'
    context_block.accepts.append('CustomStaff')

    current_function_name = systemtools.TestManager.get_current_function_name()
    systemtools.TestManager.write_test_output(lilypond_file, __file__, current_function_name)
    assert format(score) == systemtools.TestManager.read_test_output(__file__, current_function_name)
