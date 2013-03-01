from experimental import *
import py


def test_SegmentSpecification__select_beats_01():
    '''Set red segment divisions to red segment beats.
    Set blue segment divisions to blue segment beats.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_rhythm(library.sixteenths)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_beats = blue_segment.select_beats('Voice 1')
    blue_segment.set_divisions(blue_beats)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_02():
    '''Set both segments' divisions to red segment beats.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_rhythm(library.sixteenths)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_segment.set_divisions(red_beats)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_03():
    '''Set both segments' divisions to blue segment beats.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')
    score_specification.set_rhythm(library.sixteenths)
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    blue_beats = blue_segment.select_beats('Voice 1')
    red_segment.set_divisions(blue_beats)
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_segment.set_divisions(blue_beats)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_04():
    '''Single-integer positive beat getitem index.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_rhythm(library.sixteenths)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_beats = blue_segment.select_beats('Voice 1')
    blue_segment.set_divisions(blue_beats)
    beat = blue_segment.select_beats('Voice 1')[2]
    beat.timespan.select_leaves('Voice 1').set_spanner(spannertools.SlurSpanner())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)


def test_SegmentSpecification__select_beats_05():
    '''Single-integer negative beat getitem index.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecificationInterface(score_template)
    score_specification.set_rhythm(library.sixteenths)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 8), (2, 4)])
    red_beats = red_segment.select_beats('Voice 1')
    red_segment.set_divisions(red_beats)
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_time_signatures([(1, 4), (4, 8)])
    blue_beats = blue_segment.select_beats('Voice 1')
    blue_segment.set_divisions(blue_beats)
    beat = blue_segment.select_beats('Voice 1')[-2]
    beat.timespan.select_leaves('Voice 1').set_spanner(spannertools.SlurSpanner())
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    testtools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == testtools.read_test_output(__file__, current_function_name)
