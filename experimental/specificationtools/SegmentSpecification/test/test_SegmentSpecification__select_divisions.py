from abjad import *
from experimental import *
import py


def test_SegmentSpecification__select_divisions_01():
    py.test.skip('FIXME')

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)

    red_segment = score_specification.append_segment(name='red')
    blue_segment = score_specification.append_segment(name='blue')

    red_segment.set_time_signatures(2 * [(3, 8)])
    red_segment.set_divisions([(4, 8)])
    divisions_starting_in_red = red_segment.select_divisions()
    # this raises partition error during interpretation but shouldn't
    red_segment.set_rhythm(library.sixteenths, selector=divisions_starting_in_red)
