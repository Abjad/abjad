from abjad import *
from experimental.tools import *
import py


# NEXT TODO: make this work
def test_CounttimeComponentSelector__payload_callbacks_01():
    '''Slice leaves.
    '''
    py.test.skip('working on this one now.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    red_leaves = red_segment.select_leaves('Voice 1')
    red_leaves = red_leaves[5:10]
    blue_segment = score_specification.append_segment(name='blue')
    blue_segment.set_rhythm(red_leaves)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name, render_pdf=True)
    #assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


#def test_CounttimeComponentSelector__payload_callbacks_02():
#    '''Partition beats by ratio.
#    '''
#
#    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
#    score_specification = specificationtools.ScoreSpecification(score_template)
#    red_segment = score_specification.append_segment(name='red')
#    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
#    beats = red_segment.select_beats('Voice 1')
#    red_segment.set_divisions(beats)
#    left, right = beats.partition_by_ratio((1, 1))
#    left.set_rhythm(library.sixteenths)
#    right.set_rhythm(library.thirty_seconds)
#    score = score_specification.interpret()
#
#    current_function_name = introspectiontools.get_current_function_name()
#    helpertools.write_test_output(score, __file__, current_function_name)
#    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
#
#
#def test_CounttimeComponentSelector__payload_callbacks_03():
#    '''Partition beats by ratio of durations.
#    '''
#
#    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
#    score_specification = specificationtools.ScoreSpecification(score_template)
#    red_segment = score_specification.append_segment(name='red')
#    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
#    beats = red_segment.select_beats('Voice 1')
#    red_segment.set_divisions(beats)
#    left, right = beats.partition_by_ratio_of_durations((1, 1))
#    left.set_rhythm(library.sixteenths)
#    right.set_rhythm(library.thirty_seconds)
#    score = score_specification.interpret()
#
#    current_function_name = introspectiontools.get_current_function_name()
#    helpertools.write_test_output(score, __file__, current_function_name)
#    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
#
#
#def test_CounttimeComponentSelector__payload_callbacks_04():
#    '''Repeat to duration.
#    '''
#
#    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
#    score_specification = specificationtools.ScoreSpecification(score_template)
#    red_segment = score_specification.append_segment(name='red')
#    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
#    beats = red_segment.select_beats('Voice 1')
#    beats = beats.repeat_to_duration(Duration(5, 8))
#    red_segment.set_divisions(beats)
#    red_segment.set_rhythm(library.sixteenths)
#    score = score_specification.interpret()
#
#    current_function_name = introspectiontools.get_current_function_name()
#    helpertools.write_test_output(score, __file__, current_function_name)
#    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
#
#
#def test_CounttimeComponentSelector__payload_callbacks_05():
#    '''Repeat to length.
#    '''
#
#    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
#    score_specification = specificationtools.ScoreSpecification(score_template)
#    red_segment = score_specification.append_segment(name='red')
#    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
#    beats = red_segment.select_beats('Voice 1')
#    beats = beats.repeat_to_length(3)
#    red_segment.set_divisions(beats)
#    red_segment.set_rhythm(library.sixteenths)
#    score = score_specification.interpret()
#
#    current_function_name = introspectiontools.get_current_function_name()
#    helpertools.write_test_output(score, __file__, current_function_name)
#    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
#
#
#def test_CounttimeComponentSelector__payload_callbacks_06():
#    '''Reverse beats.
#    '''
#
#    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
#    score_specification = specificationtools.ScoreSpecification(score_template)
#    red_segment = score_specification.append_segment(name='red')
#    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
#    beats = red_segment.select_beats('Voice 1')
#    beats = beats.reverse()
#    red_segment.set_divisions(beats)
#    red_segment.set_rhythm(library.sixteenths)
#    score = score_specification.interpret()
#
#    current_function_name = introspectiontools.get_current_function_name()
#    helpertools.write_test_output(score, __file__, current_function_name)
#    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
#
#
#def test_CounttimeComponentSelector__payload_callbacks_07():
#    '''Rotate beats.
#    '''
#
#    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
#    score_specification = specificationtools.ScoreSpecification(score_template)
#    red_segment = score_specification.append_segment(name='red')
#    red_segment.set_time_signatures([(2, 4), (3, 8), (3, 4)])
#    beats = red_segment.select_beats('Voice 1')
#    beats = beats.rotate(-1)
#    red_segment.set_divisions(beats)
#    red_segment.set_rhythm(library.sixteenths)
#    score = score_specification.interpret()
#
#    current_function_name = introspectiontools.get_current_function_name()
#    helpertools.write_test_output(score, __file__, current_function_name)
#    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
