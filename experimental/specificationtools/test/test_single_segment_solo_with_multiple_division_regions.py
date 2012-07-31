from abjad.tools import *
from experimental import *
from experimental.specificationtools import library
import py


def test_single_segment_solo_with_multiple_division_regions_01():
    '''Three measures and three division regions.
    One division region per measure.
    Selection handle by measure index.
    '''
    py.test.skip('current working on this one.')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment('red')
    #red_segment.set_time_signatures()
