from abjad.tools import *
from experimental.selectortools.SegmentSelector import SegmentSelector
from experimental.specificationtools.Setting import Setting
from experimental.specificationtools.SettingInventory import SettingInventory
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.selectortools.Selection import Selection
from experimental.timespantools.Timepoint import Timepoint
from experimental.timespantools.Timespan import Timespan


def test_SettingInventory___repr___01():
    '''Repr is evaluable.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives
    directive_inventory_2 = eval(repr(directive_inventory_1))

    assert isinstance(directive_inventory_1, SettingInventory)
    assert isinstance(directive_inventory_2, SettingInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2
