from experimental import *


def test_ScoreSpecification__set_markup_01():
    '''Set markup.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(1, 4)], contexts=['Voice 1'])
    score_specification.set_rhythm(library.note_tokens)
    markup = markuptools.Markup(r'\italic { staccatissimo }')
    score_specification.select_leaves('Voice 1').set_markup(markup)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_markup_02():
    '''Set markup from string.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = musicexpressiontools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(1, 4)], contexts=['Voice 1'])
    score_specification.set_rhythm(library.note_tokens)
    score_specification.select_leaves('Voice 1').set_markup('stacc.')
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
