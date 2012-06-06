from abjad.tools import *
from baca.specificationtools.SettingInventory import SettingInventory
from baca.specificationtools.ScoreSpecification import ScoreSpecification


def test_SettingInventory___init___01():
    '''Init from other setting inventory.
    '''

    specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])

    setting_inventory_1 = segment.settings
    setting_inventory_2 = SettingInventory(setting_inventory_1)

    assert isinstance(setting_inventory_1, SettingInventory)
    assert isinstance(setting_inventory_2, SettingInventory)
    assert not setting_inventory_1 is setting_inventory_2
    assert setting_inventory_1 == setting_inventory_2
