from abjad.tools import *
from experimental.tools import *
from experimental.tools.settingtools.SingleContextSetting import SingleContextSetting
from experimental.tools.settingtools.SingleContextSettingInventory import SingleContextSettingInventory
from experimental.tools.specificationtools.ScoreSpecification import ScoreSpecification


def test_SingleContextSettingInventory___repr___01():
    '''Repr is evaluable.
    '''

    score_template = scoretemplatetools.GroupedRhythmicStavesScoreTemplate(staff_count=1)
    score_specification = specificationtools.ScoreSpecification(score_template)
    red_segment = score_specification.append_segment(name='red')
    red_segment.set_time_signatures([(4, 8), (3, 8)])

    setting_inventory_1 = score_specification['red'].single_context_settings
    setting_inventory_2 = eval(repr(setting_inventory_1))

    assert isinstance(setting_inventory_1, SingleContextSettingInventory)
    assert isinstance(setting_inventory_2, SingleContextSettingInventory)
    assert not setting_inventory_1 is setting_inventory_2
    assert setting_inventory_1 == setting_inventory_2
