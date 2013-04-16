from experimental import *
from abjad.tools.scoretemplatetools.ScoreTemplate import ScoreTemplate


def test_custom_contexts_01():

    class CustomContextScoreTemplate(ScoreTemplate):

        ### INITIALIZER ###

        def __init__(self):
            pass

        ### SPECIAL METHODS ###

        def __call__(self):
            custom_voice = voicetools.Voice(context_name='CustomVoice', name='Custom Voice')
            custom_staff = stafftools.Staff(context_name='CustomStaff', name='Custom Staff')
            custom_score = scoretools.Score(name='Custom Score')
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
    context_block.override.beam.color = 'green'
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

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(lilypond_file, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
