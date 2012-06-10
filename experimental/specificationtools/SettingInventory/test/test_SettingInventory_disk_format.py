from abjad.tools import *
from experimental import specificationtools
from experimental.specificationtools import library
from experimental.specificationtools import ScoreSpecification
from experimental.specificationtools import SettingInventory


def test_SettingInventory_disk_format_01():
    '''Disk format exists and is evaluable.
    '''

    score_specification = ScoreSpecification(scoretemplatetools.GroupedRhythmicStavesScoreTemplate(n=1))
    segment = score_specification.append_segment()
    segment.set_time_signatures(segment, [(4, 8), (3, 8)])
    score_specification.interpret()

    setting_inventory_1 = segment.settings

    disk_format = setting_inventory_1._disk_format

    r'''
    specificationtools.SettingInventory([
        specificationtools.Setting(
            '1',
            None,
            None,
            'time_signatures',
            [(4, 8), (3, 8)],
            True,
            False,
            fresh=True
            )
        ])
    '''

    assert disk_format == "specificationtools.SettingInventory([\n\tspecificationtools.Setting(\n\t\t'1',\n\t\tNone,\n\t\tNone,\n\t\t'time_signatures',\n\t\t[(4, 8), (3, 8)],\n\t\tTrue,\n\t\tFalse,\n\t\tfresh=True\n\t\t)\n\t])"

    setting_inventory_2 = eval(disk_format)

    assert isinstance(setting_inventory_1, SettingInventory)
    assert isinstance(setting_inventory_2, SettingInventory)
    assert not setting_inventory_1 is setting_inventory_2
    assert setting_inventory_1 == setting_inventory_2
