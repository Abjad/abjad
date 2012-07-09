from abjad.tools import *
from experimental.specificationtools.ContextSetting import ContextSetting
from experimental.specificationtools.ContextSettingInventory import ContextSettingInventory
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.selectortools.MultipleContextSelection import MultipleContextSelection


def test_ContextSettingInventory___repr___01():
    '''Repr is evaluable.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    setting_inventory_1 = segment.settings
    setting_inventory_2 = eval(repr(setting_inventory_1))

    assert isinstance(setting_inventory_1, ContextSettingInventory)
    assert isinstance(setting_inventory_2, ContextSettingInventory)
    assert not setting_inventory_1 is setting_inventory_2
    assert setting_inventory_1 == setting_inventory_2
