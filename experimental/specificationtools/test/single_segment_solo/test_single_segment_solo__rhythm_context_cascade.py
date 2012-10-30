from abjad import *
from experimental import *


def test_single_segment_solo__rhythm_context_cascade_01():
    '''Settings made against lower-level contexts override 
    settings made against higher-level contexts.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)
    segment.set_rhythm(library.note_filled_tokens, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__rhythm_context_cascade_02():
    '''Thirty-seconds override sixteenths.
    Then note-filled tokens override thirty-seconds.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)
    segment.set_rhythm(library.thirty_seconds)
    segment.set_rhythm(library.note_filled_tokens, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__rhythm_context_cascade_03():
    '''Thirty-seconds override sixteenths.
    Then note-filled tokens override thirty-seconds.
    Then rest-filled tokens override note-filled tokens.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)
    segment.set_rhythm(library.thirty_seconds)
    segment.set_rhythm(library.note_filled_tokens, contexts=['Voice 1'])
    segment.set_rhythm(library.rest_filled_tokens, contexts=['Voice 1'])
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__rhythm_context_cascade_04():
    '''Lexically later settings don't matter if they 
    are made against a higher-level context.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.note_filled_tokens, contexts=['Voice 1'])
    segment.set_rhythm(library.rest_filled_tokens, contexts=['Voice 1'])
    segment.set_rhythm(library.sixteenths)
    segment.set_rhythm(library.thirty_seconds)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_single_segment_solo__rhythm_context_cascade_05():
    '''Selector and contexts work together.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    segment = score_specification.make_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8)])
    segment.set_divisions([(3, 16)])
    segment.set_rhythm(library.sixteenths)
    selector = segment.select_background_measure(1)
    segment.set_rhythm(library.thirty_seconds, contexts=['Voice 1'], selector=selector)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
