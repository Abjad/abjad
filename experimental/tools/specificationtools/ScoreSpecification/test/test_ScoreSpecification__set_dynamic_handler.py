from experimental import *


def test_ScoreSpecification__set_dynamic_handler_01():
    '''Set handler on all leaves in voice.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False)
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    handler = library.hairpins.new(('pp', '<', 'p'))
    score_specification.select_leaves('Voice 1').set_dynamic_handler(handler)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_dynamic_handler_02():
    '''Set handler on leaf slice.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False)
    score_specification.set_rhythm(library.note_tokens, contexts=['Voice 1'])
    handler = library.hairpins.new(('pp', '<', 'p'))
    score_specification.select_leaves('Voice 1')[2:5].set_dynamic_handler(handler)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_ScoreSpecification__set_dynamic_handler_03():
    '''Set handler on division slice.
    '''

    score_template = scoretemplatetools.GroupedStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_time_signatures(5 * [(2, 8)])
    score_specification.set_divisions([(3, 16)], contexts=['Voice 1'])
    rhythm = library.sixteenths.new(beam_cells_together=False)
    score_specification.set_rhythm(library.sixteenths, contexts=['Voice 1'])
    handler = library.hairpins.new(('p', '<', 'f'))
    divisions = score_specification.select_divisions('Voice 1')[2:5]
    divisions.timespan.select_leaves('Voice 1').set_dynamic_handler(handler)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
