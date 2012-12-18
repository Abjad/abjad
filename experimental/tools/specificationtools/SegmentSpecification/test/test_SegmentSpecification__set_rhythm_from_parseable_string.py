from abjad import *
from experimental.tools import *
import py


def test_SegmentSpecification__set_rhythm_from_parseable_string_01():

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 8), (3, 8)])
    red_segment.set_rhythm("{ c'16 [ ( c'8 c'8. ] ) }")
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__set_rhythm_from_parseable_string_02():
    '''With set-time reverse.
    '''
    py.test.skip('implement statalservertools.make_source() eventually.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 8), (3, 8)])
    rhythm = statalservertools.make_source("{ c'16 [ ( c'8 c'8. ] ) }")
    red_segment.set_rhythm(rhythm.REVERSE())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__set_rhythm_from_parseable_string_03():
    '''With set-time rotation.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 8), (3, 8)])
    rotation = settingtools.RotationIndicator(-1, fracture_spanners=False)
    red_segment.set_rhythm("{ c'16 [ ( c'8 c'8. ] ) }", rotation=rotation)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
