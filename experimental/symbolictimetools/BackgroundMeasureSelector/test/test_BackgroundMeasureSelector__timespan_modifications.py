from abjad import *
from experimental import *


def test_BackgroundMeasureSelector__timespan_modifications_01():
    '''Scale timespan.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    timespan = red_segment.select_background_measures(0, 1)
    timespan = timespan.scale_timespan(Multiplier(4))
    red_segment.set_rhythm(library.thirty_seconds, timespan=timespan)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__timespan_modifications_02():
    '''Set timespan duration.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    timespan = red_segment.select_background_measures(0, 1)
    timespan = timespan.set_timespan_duration(Duration(2, 8))
    red_segment.set_rhythm(library.thirty_seconds, timespan=timespan)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__timespan_modifications_03():
    '''Set timespan start offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    timespan = red_segment.select_background_measures(0, 2)
    timespan = timespan.set_timespan_start_offset(Offset(1, 8))
    red_segment.set_rhythm(library.thirty_seconds, timespan=timespan)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__timespan_modifications_04():
    '''Set timespan stop offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    timespan = red_segment.select_background_measures(0, 1)
    timespan = timespan.set_timespan_stop_offset(Offset(2, 8))
    red_segment.set_rhythm(library.thirty_seconds, timespan=timespan)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__timespan_modifications_05():
    '''Translate timespan.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    timespan = red_segment.select_background_measures(0, 1)
    timespan = timespan.translate_timespan(Duration(1, 8)) 
    red_segment.set_rhythm(library.thirty_seconds, timespan=timespan)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__timespan_modifications_06():
    '''Translate timespan start offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    timespan = red_segment.select_background_measures(0, 2)
    timespan = timespan.translate_timespan_start_offset(Duration(1, 8)) 
    red_segment.set_rhythm(library.thirty_seconds, timespan=timespan)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__timespan_modifications_07():
    '''Translate timespan stop offset.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    timespan = red_segment.select_background_measures(0, 2)
    timespan = timespan.translate_timespan_stop_offset(Duration(-1, 8)) 
    red_segment.set_rhythm(library.thirty_seconds, timespan=timespan)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)


def test_BackgroundMeasureSelector__timespan_modifications_08():
    '''Stacked timespan modifications applied in composition.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(1, 8), (2, 8), (3, 8)])
    red_segment.set_divisions([(1, 8)])
    red_segment.set_rhythm(library.sixteenths)
    timespan = red_segment.select_background_measures(0, 2)
    timespan = timespan.translate_timespan_start_offset(Duration(1, 8))
    timespan = timespan.scale_timespan(Multiplier(2))
    red_segment.set_rhythm(library.thirty_seconds, timespan=timespan)
    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
