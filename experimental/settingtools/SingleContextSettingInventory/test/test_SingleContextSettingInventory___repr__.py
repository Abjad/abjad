from abjad.tools import *
from experimental.settingtools.SingleContextSetting import SingleContextSetting
from experimental.settingtools.SingleContextSettingInventory import SingleContextSettingInventory
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.selectortools.MultipleContextTimespanSelector import MultipleContextTimespanSelector


def test_SingleContextSettingInventory___repr___01():
    '''Repr is evaluable.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    specification = ScoreSpecification(score_template)

    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    setting_inventory_1 = segment.single_context_settings
    setting_inventory_2 = eval(repr(setting_inventory_1))

    assert isinstance(setting_inventory_1, SingleContextSettingInventory)
    assert isinstance(setting_inventory_2, SingleContextSettingInventory)
    assert not setting_inventory_1 is setting_inventory_2
    assert setting_inventory_1 == setting_inventory_2
