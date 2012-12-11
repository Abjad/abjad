from abjad import *
from experimental import *
import py
py.test.skip('deprecated.')


def test_BackgroundMeasureSelector__get_selected_objects_01():

    template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])
    measures = red_segment.select_background_measures()
    score = score_specification.interpret()
    
    result = measures.get_selected_objects(score_specification, 'Voice 1')
    assert result == [mathtools.NonreducedFraction(4, 8), mathtools.NonreducedFraction(3, 8)]
