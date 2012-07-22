from abjad.tools import *
from experimental.settingtools.MultipleContextSettingInventory import MultipleContextSettingInventory
from experimental.specificationtools.ScoreSpecification import ScoreSpecification


def test_MultipleContextSettingInventory___init___01():
    '''Init from other directive inventory.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)

    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    directive_inventory_1 = segment.directives
    directive_inventory_2 = MultipleContextSettingInventory(directive_inventory_1)

    assert isinstance(directive_inventory_1, MultipleContextSettingInventory)
    assert isinstance(directive_inventory_2, MultipleContextSettingInventory)
    assert not directive_inventory_1 is directive_inventory_2
    assert directive_inventory_1 == directive_inventory_2
