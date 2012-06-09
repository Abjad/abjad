from abjad.tools import *
from experimental.specificationtools.Setting import Setting
from experimental.specificationtools.SettingInventory import SettingInventory
from experimental.specificationtools.ScoreSpecification import ScoreSpecification
from experimental.specificationtools.Selection import Selection


def test_SettingInventory___repr___01():
    '''Repr is evaluable.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    setting_inventory_1 = segment.settings
    setting_inventory_2 = eval(repr(setting_inventory_1))

    assert isinstance(setting_inventory_1, SettingInventory)
    assert isinstance(setting_inventory_2, SettingInventory)
    assert not setting_inventory_1 is setting_inventory_2
    assert setting_inventory_1 == setting_inventory_2
