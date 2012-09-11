from experimental import *


def test_SegmentSpecification_request_division_command_01():
    '''Request division command active at 1/8 into measure 2 in earlier segment.
    Request only first element of command.
    '''
    
    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    segment = score_specification.append_segment(name='red')
    segment.set_time_signatures([(4, 8), (3, 8), (2, 8), (4, 8)])
    segment.set_divisions([(4, 16)])
    selector = segment.select_background_measures(1, 3)
    segment.set_divisions([(2, 16), (3, 16)], selector=selector)
    segment.set_rhythm(library.sixteenths)

    selector = segment.select_background_measure(2)
    addendum = durationtools.Offset(1, 8)
    source = segment.request_division_command(selector=selector, addendum=addendum, count=1)

    segment = score_specification.append_segment(name='blue')
    segment.set_divisions(source)

    score = score_specification.interpret()

    current_function_name = introspectiontools.get_current_function_name()
    helpertools.write_test_output(score, __file__, current_function_name)
    assert score.lilypond_format == helpertools.read_test_output(__file__, current_function_name)
